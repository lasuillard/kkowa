import atexit
from logging import getLogger
from typing import Annotated

import typer
from opentelemetry import _logs, metrics, trace
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient, GrpcInstrumentorServer
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from src import app

from . import common


def _app(
    ipc_address: Annotated[
        str,
        typer.Option(
            help=(
                "IPC address. By default it create UNIX Domain Socket internally."
                " If provided would expose IPC server to network, allowing external applications to access."
            ),
        ),
    ] = "",
) -> None:
    """Start GUI application."""
    # TODO(lasuillard): Initialize logging config first

    # Initialize telemetry providers
    atexit.register(_init_tracer().shutdown)
    atexit.register(_init_metrics().shutdown)
    atexit.register(_init_logs().shutdown)

    # Launch app
    app.run(ipc_address=ipc_address)


def register(app: typer.Typer) -> None:
    """Register commands in current module to given `Typer` app."""
    app.command(
        name="app",
        context_settings={
            "auto_envvar_prefix": common.ENV_VAR_PREFIX,
        },
    )(_app)


def _init_tracer() -> TracerProvider:
    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter()),
    )
    trace.set_tracer_provider(tracer_provider)

    GrpcInstrumentorClient().instrument()
    GrpcInstrumentorServer().instrument()

    return tracer_provider


def _init_metrics() -> MeterProvider:
    meter_provider = MeterProvider(
        metric_readers=[
            PeriodicExportingMetricReader(OTLPMetricExporter()),
        ],
    )
    metrics.set_meter_provider(meter_provider)

    return meter_provider


def _init_logs() -> LoggerProvider:
    logger_provider = LoggerProvider()
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(OTLPLogExporter(insecure=True)),
    )
    _logs.set_logger_provider(logger_provider)

    # Add export handler to root logger
    getLogger().addHandler(LoggingHandler())

    return logger_provider

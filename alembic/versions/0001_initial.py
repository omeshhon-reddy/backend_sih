from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("report", sa.String(length=200), nullable=False),
        sa.Column("report_description", sa.Text(), nullable=False),
        sa.Column("elevation_m", sa.Float(), nullable=True),
        sa.Column("slope_degrees", sa.Float(), nullable=True),
        sa.Column("aspect_degrees", sa.Float(), nullable=True),
        sa.Column("rainfall_1d_before", sa.Float(), nullable=True),
        sa.Column("rainfall_3d_before", sa.Float(), nullable=True),
        sa.Column("rainfall_7d_before", sa.Float(), nullable=True),
        sa.Column("rainfall_14d_before", sa.Float(), nullable=True),
        sa.Column("rainfall_30d_before", sa.Float(), nullable=True),
        sa.Column("rainfall_7d_max1d", sa.Float(), nullable=True),
        sa.Column("rainfall_3d_over_7d_ratio", sa.Float(), nullable=True),
        sa.Column("soil_moisture", sa.Float(), nullable=True),
        sa.Column("soil_moisture_available", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_reports_longitude", "reports", ["longitude"])
    op.create_index("ix_reports_latitude", "reports", ["latitude"])
    op.create_index("ix_reports_created_at", "reports", ["created_at"])

    op.create_table(
        "risk_predictions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("report_id", sa.Uuid(as_uuid=True), sa.ForeignKey("reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("risk_level", sa.Integer(), nullable=False),
        sa.Column("risk_tier", sa.String(length=16), nullable=False),
        sa.Column("alert_triggered", sa.Boolean(), nullable=False),
        sa.Column("alert_message", sa.Text(), nullable=False),
        sa.Column("model_version", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_risk_predictions_report_id", "risk_predictions", ["report_id"])
    op.create_index("ix_risk_predictions_risk_tier", "risk_predictions", ["risk_tier"])
    op.create_index("ix_risk_predictions_created_at", "risk_predictions", ["created_at"])

    op.create_table(
        "alerts",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("report_id", sa.Uuid(as_uuid=True), sa.ForeignKey("reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "risk_prediction_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("risk_predictions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("alert_type", sa.String(length=32), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_alerts_report_id", "alerts", ["report_id"])
    op.create_index("ix_alerts_risk_prediction_id", "alerts", ["risk_prediction_id"])
    op.create_index("ix_alerts_created_at", "alerts", ["created_at"])


def downgrade() -> None:
    op.drop_table("alerts")
    op.drop_table("risk_predictions")
    op.drop_table("reports")

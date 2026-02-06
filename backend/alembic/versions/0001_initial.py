"""initial schema"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "brands",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("niche", sa.String, nullable=False),
        sa.Column("target_audience", sa.String, nullable=False),
        sa.Column("tone", sa.String, nullable=False),
        sa.Column("brand_colors", sa.JSON, nullable=False),
        sa.Column("fonts", sa.JSON, nullable=False),
        sa.Column("logo_url", sa.String),
        sa.Column("watermark_text", sa.String),
        sa.Column("watermark_opacity", sa.Integer, default=40),
        sa.Column("banned_words", sa.JSON, nullable=False),
        sa.Column("preferred_cta", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "brand_assets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("brand_id", sa.Integer, sa.ForeignKey("brands.id"), nullable=False),
        sa.Column("asset_type", sa.String, nullable=False),
        sa.Column("file_url", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "connected_accounts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("provider", sa.String, nullable=False),
        sa.Column("account_name", sa.String, nullable=False),
        sa.Column("access_token", sa.Text, nullable=False),
        sa.Column("refresh_token", sa.Text),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "templates",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("size", sa.String, nullable=False),
        sa.Column("layout_config", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "posters",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("brand_id", sa.Integer, sa.ForeignKey("brands.id"), nullable=False),
        sa.Column("template_id", sa.Integer, sa.ForeignKey("templates.id"), nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("image_url", sa.String, nullable=False),
        sa.Column("size", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "captions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("poster_id", sa.Integer, sa.ForeignKey("posters.id"), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("hashtags", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "campaigns",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("brand_id", sa.Integer, sa.ForeignKey("brands.id"), nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("duration_days", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "campaign_items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("campaign_id", sa.Integer, sa.ForeignKey("campaigns.id"), nullable=False),
        sa.Column("day_index", sa.Integer, nullable=False),
        sa.Column("poster_id", sa.Integer, sa.ForeignKey("posters.id"), nullable=False),
        sa.Column("caption_id", sa.Integer, sa.ForeignKey("captions.id"), nullable=False),
        sa.Column("scheduled_time", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "scheduled_posts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("brand_id", sa.Integer, sa.ForeignKey("brands.id"), nullable=False),
        sa.Column("poster_id", sa.Integer, sa.ForeignKey("posters.id"), nullable=False),
        sa.Column("caption_id", sa.Integer, sa.ForeignKey("captions.id"), nullable=False),
        sa.Column("platforms", sa.JSON, nullable=False),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=False),
        sa.Column("published", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "post_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("scheduled_post_id", sa.Integer, sa.ForeignKey("scheduled_posts.id"), nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("detail", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "analytics_metrics",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("scheduled_post_id", sa.Integer, sa.ForeignKey("scheduled_posts.id"), nullable=False),
        sa.Column("impressions", sa.Integer, default=0),
        sa.Column("clicks", sa.Integer, default=0),
        sa.Column("likes", sa.Integer, default=0),
        sa.Column("comments", sa.Integer, default=0),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "ai_suggestions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("brand_id", sa.Integer, sa.ForeignKey("brands.id"), nullable=False),
        sa.Column("suggestion_type", sa.String, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("ai_suggestions")
    op.drop_table("analytics_metrics")
    op.drop_table("post_logs")
    op.drop_table("scheduled_posts")
    op.drop_table("campaign_items")
    op.drop_table("campaigns")
    op.drop_table("captions")
    op.drop_table("posters")
    op.drop_table("templates")
    op.drop_table("connected_accounts")
    op.drop_table("brand_assets")
    op.drop_table("brands")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

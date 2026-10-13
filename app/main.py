"""fitness-ai 应用入口。

第 0 周只放一个最小可运行的 FastAPI 骨架，用来验证环境是否搭好。
第 1-6 周会逐步把训练记录、排行榜、AI 周报等功能加进来。
"""

from datetime import datetime

from fastapi import FastAPI

app = FastAPI(
    title="fitness-ai",
    description="健身训练记录系统 · 逐步演进为 AI 私教 Agent",
    version="0.0.1",
)


@app.get("/", summary="服务健康检查")
def root() -> dict:
    """返回服务基本信息，用于确认服务已启动。"""
    return {
        "app": "fitness-ai",
        "version": app.version,
        "status": "ok",
        "time": datetime.now().isoformat(timespec="seconds"),
        "docs": "/docs",
    }


@app.get("/health", summary="健康检查")
def health() -> dict:
    """给部署和监控用的健康检查接口。"""
    return {"status": "healthy"}

#!/usr/bin/env python3
"""
Docsify -> VitePress migration script.

Moves and renames markdown files, fixes image paths and cross-links.
Usage: python scripts/migrate.py [--dry-run]
"""

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# ── File mapping: source (relative to ROOT) -> dest (relative to ROOT) ──

CHAPTER_MAP = {
    # Stage 1: Foundation
    "1-1-大模型认知与工程概览.md": "docs/stage1-foundation/ch01-1.md",
    "1-2-提示词工程基础.md": "docs/stage1-foundation/ch01-2.md",
    "1-3-RAG、微调、续训与智能体选型.md": "docs/stage1-foundation/ch01-3.md",
    "2-RAG-搭建企业私有&个人知识库.md": "docs/stage1-foundation/ch02.md",
    # Stage 2: Low-code
    "3-基于Coze&Dify平台的智能体开发.md": "docs/stage2-lowcode/ch03.md",
    "4-Python调用Dify平台工作流.md": "docs/stage2-lowcode/ch04.md",
    "5-Python调用Coze平台工作流.md": "docs/stage2-lowcode/ch05.md",
    "6-Coze与Dify的Windows平台部署.md": "docs/stage2-lowcode/ch06.md",
    "7-企业级大模型部署.md": "docs/stage2-lowcode/ch07.md",
    "8-Docker入门与Dify部署常见问题.md": "docs/stage2-lowcode/ch08.md",
    # Stage 3: Framework
    "9-LangChain概述与架构.md": "docs/stage3-framework/ch09.md",
    "10-LangChain快速上手与HelloWorld.md": "docs/stage3-framework/ch10.md",
    "11-Model-I-O与模型接入.md": "docs/stage3-framework/ch11.md",
    "12-Ollama本地部署与调用.md": "docs/stage3-framework/ch12.md",
    "13-提示词与消息模板.md": "docs/stage3-framework/ch13.md",
    "14-输出解析器.md": "docs/stage3-framework/ch14.md",
    "15-LCEL与链式调用.md": "docs/stage3-framework/ch15.md",
    "16-记忆与对话历史（含Redis基础）.md": "docs/stage3-framework/ch16.md",
    "17-Tools工具调用.md": "docs/stage3-framework/ch17.md",
    "18-向量数据库与Embedding实战.md": "docs/stage3-framework/ch18.md",
    "19-RAG检索增强生成.md": "docs/stage3-framework/ch19.md",
    "20-MCP模型上下文协议.md": "docs/stage3-framework/ch20.md",
    "21-Agent智能体.md": "docs/stage3-framework/ch21.md",
    "22-LangGraph概述与快速入门.md": "docs/stage3-framework/ch22.md",
    "23-LangGraphAPI：图与状态.md": "docs/stage3-framework/ch23.md",
    "24-LangGraphAPI：节点、边与进阶.md": "docs/stage3-framework/ch24.md",
    "25-LangGraph高级特性.md": "docs/stage3-framework/ch25.md",
    "26-LangGraph多智能体与A2A.md": "docs/stage3-framework/ch26.md",
    "27-Skills技能与AI编程工具实践.md": "docs/stage3-framework/ch27.md",
}

GUIDE_MAP = {
    "教程目录大纲.md": "docs/guide/outline.md",
    "全书术语表.md": "docs/guide/glossary.md",
    "新手入门与常见问题.md": "docs/guide/faq.md",
    "工具导航与参考资料索引.md": "docs/guide/resources.md",
    "教程案例链接汇总.md": "docs/guide/case-links.md",
    "AI智能体与大模型应用开发面试题库.md": "docs/guide/interview.md",
    "教程更新日志.md": "docs/guide/changelog.md",
    "CONTRIBUTING.md": "docs/guide/contributing.md",
}

CASE_MAP = {
    "案例与源码-1-Coze&Dify工作流智能体/3.1-Coze案例：一键生成行业调研PPT/3.1-一键生成行业调研PPT.md": "docs/stage2-lowcode/cases/case-3.1.md",
    "案例与源码-1-Coze&Dify工作流智能体/3.2-Coze案例：复刻爆款视频/3.2-复刻爆款视频.md": "docs/stage2-lowcode/cases/case-3.2.md",
    "案例与源码-1-Coze&Dify工作流智能体/3.3-Coze案例：产品营销海报生成/3.3-产品营销海报生成.md": "docs/stage2-lowcode/cases/case-3.3.md",
    "案例与源码-1-Coze&Dify工作流智能体/3.4-Dify案例：一键生成行业调研报告/3.4-一键生成行业调研报告.md": "docs/stage2-lowcode/cases/case-3.4.md",
    "案例与源码-1-Coze&Dify工作流智能体/3.5-Dify案例：客户投诉分类助手/3.5-客户投诉分类助手.md": "docs/stage2-lowcode/cases/case-3.5.md",
    "案例与源码-1-Coze&Dify工作流智能体/3.6-Coze案例：客服对话记录分析/3.6-客服对话记录分析-Coze.md": "docs/stage2-lowcode/cases/case-3.6.md",
    "案例与源码-1-Coze&Dify工作流智能体/3.7-Dify案例：客服对话记录分析/3.7-客服对话记录分析-Dify.md": "docs/stage2-lowcode/cases/case-3.7.md",
    "案例与源码-1-Coze&Dify工作流智能体/3.8-Coze案例：商品评论分析/3.8-商品评论分析-商品评论分析-Coze.md": "docs/stage2-lowcode/cases/case-3.8.md",
    "案例与源码-1-Coze&Dify工作流智能体/3.9-Dify案例：商品评论分析/3.9-商品评论分析-Dify.md": "docs/stage2-lowcode/cases/case-3.9.md",
    "案例与源码-1-Coze&Dify工作流智能体/3.10-Coze案例：商品营销卖点提炼/3.10-商品营销卖点提炼-Coze.md": "docs/stage2-lowcode/cases/case-3.10.md",
}

ECOMMERCE_MAP = {
    "实战项目-电商问数/0-前言.md": "docs/stage4-projects/ecommerce/index.md",
    "实战项目-电商问数/1-项目概述与数仓基础.md": "docs/stage4-projects/ecommerce/ch01.md",
    "实战项目-电商问数/2-项目整体架构与智能体流程.md": "docs/stage4-projects/ecommerce/ch02.md",
    "实战项目-电商问数/3-开发环境与基础服务准备.md": "docs/stage4-projects/ecommerce/ch03.md",
    "实战项目-电商问数/4-项目结构与基础服务配置管理.md": "docs/stage4-projects/ecommerce/ch04.md",
    "实战项目-电商问数/5-Qdrant与ES快速入门与接入.md": "docs/stage4-projects/ecommerce/ch05.md",
    "实战项目-电商问数/6-MySQL、Embedding与日志管理.md": "docs/stage4-projects/ecommerce/ch06.md",
    "实战项目-电商问数/7-元数据知识库总览与构建入口.md": "docs/stage4-projects/ecommerce/ch07.md",
    "实战项目-电商问数/8-表与字段信息同步到元数据库.md": "docs/stage4-projects/ecommerce/ch08.md",
    "实战项目-电商问数/9-字段与指标检索能力构建.md": "docs/stage4-projects/ecommerce/ch09.md",
    "实战项目-电商问数/10-问数智能体总览与工作流骨架.md": "docs/stage4-projects/ecommerce/ch10.md",
    "实战项目-电商问数/11-关键词抽取与多路召回.md": "docs/stage4-projects/ecommerce/ch11.md",
    "实战项目-电商问数/12-召回信息合并与上下文构建.md": "docs/stage4-projects/ecommerce/ch12.md",
    "实战项目-电商问数/13-SQL生成前的信息过滤与补全.md": "docs/stage4-projects/ecommerce/ch13.md",
    "实战项目-电商问数/14-SQL生成与执行闭环.md": "docs/stage4-projects/ecommerce/ch14.md",
    "实战项目-电商问数/15-API接口基础与FastAPI入门.md": "docs/stage4-projects/ecommerce/ch15.md",
    "实战项目-电商问数/16-查询接口实现与依赖组装.md": "docs/stage4-projects/ecommerce/ch16.md",
    "实战项目-电商问数/17-前后端联调与日志追踪.md": "docs/stage4-projects/ecommerce/ch17.md",
}

DEEP_RESEARCH_MAP = {
    "实战项目-深度研搜/0-前言.md": "docs/stage4-projects/deep-research/index.md",
    "实战项目-深度研搜/1-DeepAgents基础与核心概念.md": "docs/stage4-projects/deep-research/ch01.md",
    "实战项目-深度研搜/2-DeepAgents快速入门与流式解析.md": "docs/stage4-projects/deep-research/ch02.md",
    "实战项目-深度研搜/3-子智能体进阶与异步执行.md": "docs/stage4-projects/deep-research/ch03.md",
    "实战项目-深度研搜/4-接入LangGraph与LangChain.md": "docs/stage4-projects/deep-research/ch04.md",
    "实战项目-深度研搜/5-人机协作与中断恢复.md": "docs/stage4-projects/deep-research/ch05.md",
    "实战项目-深度研搜/6-长期记忆与Backend存储.md": "docs/stage4-projects/deep-research/ch06.md",
    "实战项目-深度研搜/7-中间件机制与Skills配置.md": "docs/stage4-projects/deep-research/ch07.md",
    "实战项目-深度研搜/8-项目总览与工程初始化.md": "docs/stage4-projects/deep-research/ch08.md",
    "实战项目-深度研搜/9-基础模块与模型配置.md": "docs/stage4-projects/deep-research/ch09.md",
    "实战项目-深度研搜/10-网络搜索子智能体与Tavily工具.md": "docs/stage4-projects/deep-research/ch10.md",
    "实战项目-深度研搜/11-数据库查询子智能体与MySQL工具.md": "docs/stage4-projects/deep-research/ch11.md",
    "实战项目-深度研搜/12-RAGFlow子智能体与知识库准备.md": "docs/stage4-projects/deep-research/ch12.md",
    "实战项目-深度研搜/13-主智能体搭建与异步执行.md": "docs/stage4-projects/deep-research/ch13.md",
    "实战项目-深度研搜/14-FastAPI接口与项目闭环.md": "docs/stage4-projects/deep-research/ch14.md",
}

ALL_FILE_MAP = {**CHAPTER_MAP, **GUIDE_MAP, **CASE_MAP, **ECOMMERCE_MAP, **DEEP_RESEARCH_MAP}


def build_link_map() -> dict[str, str]:
    """Build old-filename -> new VitePress path mapping for cross-link rewriting."""
    link_map: dict[str, str] = {}
    for src, dst in ALL_FILE_MAP.items():
        # Strip docs/ prefix and .md suffix for VitePress links
        vp_path = "/" + dst.removeprefix("docs/").removesuffix(".md")
        # index.md -> directory path
        if vp_path.endswith("/index"):
            vp_path = vp_path.removesuffix("/index") + "/"
        link_map[src] = vp_path
    return link_map


LINK_MAP = build_link_map()

# Directories that contain images co-located with project markdown
PROJECT_DIRS = {"docs/stage4-projects/ecommerce", "docs/stage4-projects/deep-research"}


def create_dirs(dry_run: bool):
    """Create the target directory structure."""
    dirs = [
        DOCS / ".vitepress" / "theme" / "style",
        DOCS / "public" / "images",
        DOCS / "guide",
        DOCS / "stage1-foundation",
        DOCS / "stage2-lowcode" / "cases",
        DOCS / "stage3-framework",
        DOCS / "stage4-projects" / "ecommerce",
        DOCS / "stage4-projects" / "deep-research",
        DOCS / "source-code",
    ]
    for d in dirs:
        if dry_run:
            print(f"  MKDIR {d.relative_to(ROOT)}")
        else:
            d.mkdir(parents=True, exist_ok=True)


def copy_markdown_files(dry_run: bool):
    """Copy and rename all markdown files per mapping."""
    count = 0
    for src_rel, dst_rel in ALL_FILE_MAP.items():
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.exists():
            print(f"  WARN: source not found: {src_rel}")
            continue
        if dry_run:
            print(f"  COPY {src_rel} -> {dst_rel}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        count += 1
    print(f"  Copied {count} markdown files")


def copy_images(dry_run: bool):
    """Copy image directories."""
    # Main images/ -> docs/images/
    src = ROOT / "images"
    dst = DOCS / "images"
    if src.exists():
        if dry_run:
            print(f"  COPY images/ -> docs/images/")
        else:
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

    # Banner -> public
    banner = ROOT / "images" / "banner.png"
    if banner.exists():
        dst_banner = DOCS / "public" / "images" / "banner.png"
        if dry_run:
            print(f"  COPY images/banner.png -> docs/public/images/banner.png")
        else:
            shutil.copy2(banner, dst_banner)

    # Project images (co-located)
    for proj_name, proj_dst in [
        ("实战项目-电商问数", "docs/stage4-projects/ecommerce"),
        ("实战项目-深度研搜", "docs/stage4-projects/deep-research"),
    ]:
        img_src = ROOT / proj_name / "images"
        img_dst = ROOT / proj_dst / "images"
        if img_src.exists():
            if dry_run:
                print(f"  COPY {proj_name}/images/ -> {proj_dst}/images/")
            else:
                if img_dst.exists():
                    shutil.rmtree(img_dst)
                shutil.copytree(img_src, img_dst)

    # Ecommerce yaml configs
    yaml_src = ROOT / "实战项目-电商问数" / "yaml"
    yaml_dst = ROOT / "docs/stage4-projects/ecommerce/yaml"
    if yaml_src.exists():
        if dry_run:
            print(f"  COPY 实战项目-电商问数/yaml/ -> docs/stage4-projects/ecommerce/yaml/")
        else:
            if yaml_dst.exists():
                shutil.rmtree(yaml_dst)
            shutil.copytree(yaml_src, yaml_dst)


def copy_source_code(dry_run: bool):
    """Copy source code directories (non-doc assets)."""
    mappings = [
        ("案例与源码-2-LangChain框架", "docs/source-code/langchain"),
        ("案例与源码-3-LangGraph框架", "docs/source-code/langgraph"),
    ]
    for src_name, dst_rel in mappings:
        src = ROOT / src_name
        dst = ROOT / dst_rel
        if src.exists():
            if dry_run:
                print(f"  COPY {src_name}/ -> {dst_rel}/")
            else:
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)

    # Case study 1: copy non-markdown files to source-code/coze-dify/
    case1_src = ROOT / "案例与源码-1-Coze&Dify工作流智能体"
    case1_dst = ROOT / "docs/source-code/coze-dify"
    if case1_src.exists():
        if dry_run:
            print(f"  COPY 案例与源码-1 (non-md) -> docs/source-code/coze-dify/")
        else:
            case1_dst.mkdir(parents=True, exist_ok=True)
            for item in case1_src.iterdir():
                if item.is_dir():
                    dst_sub = case1_dst / item.name
                    if dst_sub.exists():
                        shutil.rmtree(dst_sub)
                    shutil.copytree(
                        item,
                        dst_sub,
                        ignore=shutil.ignore_patterns("*.md"),
                    )


def add_frontmatter(filepath: Path, content: str) -> str:
    """Add YAML frontmatter with title extracted from H1."""
    if content.startswith("---"):
        return content

    title = ""
    for line in content.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            break

    if not title:
        title = filepath.stem

    # Escape quotes in title
    safe_title = title.replace('"', '\\"')
    frontmatter = f'---\ntitle: "{safe_title}"\n---\n\n'
    return frontmatter + content


def fix_image_paths(filepath: Path, content: str) -> str:
    """Transform image paths to VitePress absolute paths."""
    rel = str(filepath.relative_to(ROOT))

    # Project files keep relative paths (images are co-located)
    for proj_dir in PROJECT_DIRS:
        if rel.startswith(proj_dir):
            return content

    # Markdown image: ![alt](../../images/X/file) -> ![alt](/images/X/file)
    content = re.sub(
        r"(!\[[^\]]*\]\()(?:\.\./)+(images/)",
        r"\1/\2",
        content,
    )

    # Markdown image: ![alt](./images/X/file) or ![alt](images/X/file)
    content = re.sub(
        r"(!\[[^\]]*\]\()(?:\./)?images/",
        r"\1/images/",
        content,
    )

    # HTML img src: src="./images/..." or src="images/..."
    content = re.sub(
        r'(src=["\'])(?:\.\./)*(\.?/?)images/',
        r"\1/images/",
        content,
    )

    return content


def fix_cross_links(content: str) -> str:
    """Rewrite cross-links from old filenames to new VitePress paths."""
    # Sort by length descending to avoid partial matches
    sorted_entries = sorted(LINK_MAP.items(), key=lambda x: len(x[0]), reverse=True)

    for old_name, new_path in sorted_entries:
        # Handle: [text](old_name) — with or without .md extension in link
        old_escaped = re.escape(old_name)

        # [text](path/old_name.md#anchor) or [text](path/old_name.md)
        content = re.sub(
            rf"\]\((?:\.\./)*{old_escaped}(#[^)]*?)?\)",
            lambda m, np=new_path: f"]({np}{m.group(1) if m.group(1) else ''})",
            content,
        )

    # Strip Docsify-style leading underscore from anchors: #_xxx -> #xxx
    content = re.sub(r"\((/[^)]*?)#_", r"(\1#", content)

    return content


def transform_all_markdown(dry_run: bool):
    """Apply frontmatter, image path, and cross-link fixes to all docs/ markdown files."""
    count = 0
    for md_file in sorted(DOCS.rglob("*.md")):
        # Skip VitePress config directory
        if ".vitepress" in str(md_file):
            continue

        content = md_file.read_text(encoding="utf-8")
        original = content

        content = add_frontmatter(md_file, content)
        content = fix_image_paths(md_file, content)
        content = fix_cross_links(content)

        if content != original:
            if dry_run:
                print(f"  TRANSFORM {md_file.relative_to(ROOT)}")
            else:
                md_file.write_text(content, encoding="utf-8")
            count += 1

    print(f"  Transformed {count} markdown files")


def verify_images():
    """Check for broken image references."""
    broken = []
    for md_file in sorted(DOCS.rglob("*.md")):
        if ".vitepress" in str(md_file):
            continue
        content = md_file.read_text(encoding="utf-8")
        rel_path = md_file.relative_to(ROOT)

        # Find all image references
        for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", content):
            img_ref = m.group(1)
            # Skip external URLs
            if img_ref.startswith("http://") or img_ref.startswith("https://"):
                continue

            if img_ref.startswith("/"):
                # Absolute VitePress path: resolve from docs/
                img_path = DOCS / img_ref.lstrip("/")
            else:
                # Relative path: resolve from markdown file's directory
                img_path = md_file.parent / img_ref

            # Strip any anchor or query params
            img_str = str(img_path).split("#")[0].split("?")[0]
            if not Path(img_str).exists():
                broken.append((str(rel_path), img_ref))

    if broken:
        print(f"\n  WARNING: {len(broken)} broken image references found:")
        for md, img in broken[:20]:
            print(f"    {md} -> {img}")
        if len(broken) > 20:
            print(f"    ... and {len(broken) - 20} more")
    else:
        print("\n  All image references verified OK")

    return broken


def main():
    parser = argparse.ArgumentParser(description="Migrate Docsify to VitePress")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    args = parser.parse_args()

    dry_run = args.dry_run
    prefix = "[DRY RUN] " if dry_run else ""

    print(f"{prefix}Step 1: Creating directory structure...")
    create_dirs(dry_run)

    print(f"\n{prefix}Step 2: Copying markdown files...")
    copy_markdown_files(dry_run)

    print(f"\n{prefix}Step 3: Copying images...")
    copy_images(dry_run)

    print(f"\n{prefix}Step 4: Copying source code...")
    copy_source_code(dry_run)

    print(f"\n{prefix}Step 5: Transforming markdown content...")
    transform_all_markdown(dry_run)

    if not dry_run:
        print("\nStep 6: Verifying image references...")
        verify_images()

    print(f"\n{prefix}Migration complete!")


if __name__ == "__main__":
    main()

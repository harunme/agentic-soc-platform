import os
import sys
import uuid

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from mcp.server import FastMCP
from Lib.configs import BASE_DIR

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ASP.settings")
    import django

    django.setup()


    # Define UUID file path
    uuid_file_path = os.path.join(BASE_DIR, "Docker", "mcp_uuid")
    # Try to read UUID from file
    try:
        with open(uuid_file_path, 'r') as f:
            uuid_str = f.read().strip()
    except FileNotFoundError:
        # If file doesn't exist, generate new UUID and save it
        uuid_str = str(uuid.uuid1()).replace('-', "")[0:16]
        os.makedirs(os.path.dirname(uuid_file_path), exist_ok=True)
        with open(uuid_file_path, 'w') as f:
            f.write(uuid_str)

    mcp = FastMCP("ASP-MCP")
    host = "0.0.0.0"
    port = 7001
    mcp.settings.sse_path = f"/{uuid_str}/sse"
    mcp.settings.message_path = f"/{uuid_str}/messages"

    mcp.settings.host = host
    mcp.settings.port = port
    
    # add tools
    from PLUGINS.MCP.llmfunc import (
        append_artifact,
        append_enrichment,
        create_ticket,
        get_alert,
        get_alert_discussions,
        get_artifact,
        get_case,
        get_case_discussions,
        list_alerts,
        list_artifacts,
        list_cases,
        list_knowledge,
        list_playbooks,
        list_tickets,
        query_playbook_runs_by_case,
        update_alert,
        update_case,
        update_knowledge,
        update_ticket,
        siem_adaptive_query,
        siem_explore_schema,
        siem_keyword_search,
        get_current_time,
    )

    mcp.add_tool(append_artifact)
    mcp.add_tool(append_enrichment)
    mcp.add_tool(create_ticket)
    mcp.add_tool(get_alert)
    mcp.add_tool(get_alert_discussions)
    mcp.add_tool(get_artifact)
    mcp.add_tool(get_case)
    mcp.add_tool(get_case_discussions)
    mcp.add_tool(list_alerts)
    mcp.add_tool(list_artifacts)
    mcp.add_tool(list_cases)
    mcp.add_tool(list_knowledge)
    mcp.add_tool(list_playbooks)
    mcp.add_tool(list_tickets)
    mcp.add_tool(query_playbook_runs_by_case)
    mcp.add_tool(update_alert)
    mcp.add_tool(update_case)
    mcp.add_tool(update_knowledge)
    mcp.add_tool(update_ticket)
    mcp.add_tool(siem_adaptive_query)
    mcp.add_tool(siem_explore_schema)
    mcp.add_tool(siem_keyword_search)
    mcp.add_tool(get_current_time)
    
    print(f"mcp server url: http://your_server_ip:{port}/{uuid_str}/sse")
    mcp.run(transport="sse")

"""
Multi-Agent AI system for Spam Shield AI.

13 specialist/support agents + 1 orchestrator, matching the approved
architecture (Section 5):

  Specialist agents:
    url_agent, email_agent, phone_agent, message_agent, ocr_agent, qr_agent,
    domain_agents (Job/Banking/Shopping/Investment)

  Fusion/support agents:
    risk_aggregator_agent, explainability_agent, recommendation_agent

  Coordinator:
    orchestrator.Orchestrator
"""

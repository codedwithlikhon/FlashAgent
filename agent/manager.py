from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from browser_use.agent.views import AgentHistoryList

from agent.agent import get_agent
from browser.browser import browser_factory
from config.load_config import config


class BrowserAgentManager:
    def __init__(self) -> None:
        self.browser_session = browser_factory.create_shared_session(headless=True)

    async def run_task_only(
        self,
        task: str,
        model: str,
        api_key: str,
        base_url: str,
        conversation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        uid = str(uuid.uuid4())
        try:
            agent = get_agent(
                task=task,
                model=model,
                api_key=api_key,
                base_url=base_url,
                browser_session=self.browser_session,
                conversation_id=conversation_id,
            )
            history = await agent.run(max_steps=config['agent']['max_steps'])
            formatted = self._format_history(history)
            if not formatted:
                formatted = [self._get_null_response_result(model=model)]

            return {
                'uid': uid,
                'task': task,
                'status': 'finished',
                'time': datetime.now().strftime('%Y%m%d%H%M%S'),
                'total_duration_seconds': history.total_duration_seconds(),
                'total_tokens': history.total_input_tokens(),
                'is_successful': history.is_successful(),
                'is_done': history.is_done(),
                'final_browser_result': self._get_final_result(history),
                'number_of_steps': history.number_of_steps(),
                'history_all_info': self._get_all_info_history(history),
                'browser_history': formatted,
                'browser_history_screenshot': history.screenshots(),
            }
        except Exception as exc:  # noqa: BLE001
            return {
                'uid': uid,
                'task': task,
                'status': 'error',
                'time': datetime.now().strftime('%Y%m%d%H%M%S'),
                'total_duration_seconds': -1,
                'total_tokens': -1,
                'is_successful': False,
                'is_done': False,
                'final_browser_result': None,
                'number_of_steps': -1,
                'history_all_info': None,
                'browser_history': self._get_null_response_result(model=model, error=str(exc)),
                'browser_history_screenshot': [],
            }

    @staticmethod
    def _format_history(history: AgentHistoryList) -> list[Dict[str, Any]]:
        extracted_content = history.extracted_content()
        urls = history.urls()
        errors = history.errors()
        result = []
        model_outputs = history.model_outputs()
        for idx, output in enumerate(model_outputs):
            url = urls[idx] if idx < len(urls) else None
            error = errors[idx] if idx < len(errors) else None
            if output.action and output.action[-1].done is not None:
                browser_status = f"task finished: {output.action[-1].done.text}"
            else:
                browser_status = output.current_state.evaluation_previous_goal
            content = extracted_content[idx] if idx < len(extracted_content) else None
            if content and len(content) >= config['agent']['max_extracted_content_length']:
                content = None
            result.append(
                {
                    'browser_status': browser_status,
                    'extracted_content': content,
                    'url': url,
                    'error': error,
                }
            )
        return result

    @staticmethod
    def _get_all_info_history(history: AgentHistoryList) -> Dict[str, Any]:
        return {
            'action_names': history.action_names(),
            'model_thoughts': history.model_thoughts(),
            'model_outputs': history.model_outputs(),
            'model_actions': history.model_actions(),
            'action_results': history.action_results(),
            'model_actions_filtered': history.model_actions_filtered(),
        }

    @staticmethod
    def _get_final_result(history: AgentHistoryList) -> Optional[str]:
        if history.is_done():
            try:
                return history.last_action()['done']['text']
            except Exception:  # noqa: BLE001
                return 'The task failed ❌, browser tool encountered an issue.'
        return None

    @staticmethod
    def _get_null_response_result(model: str, error: str = '') -> Dict[str, Any]:
        return {
            'browser_status': 'Error',
            'extracted_content': (
                'The task failed ❌, browser tool encountered an issue. '
                f'Current agent LLM: {model}'
            ),
            'url': '',
            'error': error,
        }


browser_agent_manager = BrowserAgentManager()

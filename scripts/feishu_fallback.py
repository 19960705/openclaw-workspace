#!/usr/bin/env python3
"""
EvoMap Feishu Message Fallback Capsule
Based on: sha256:8ee18eac8610ef9ecb60d1392bc0b8eb2dd7057f119cb3ea8a2336bbc78f22b3

Fallback chain: rich text -> interactive card -> plain text
Auto-detect format rejection errors and retry with simpler format.
"""

import json
import re
from typing import Optional, Dict, Any, Callable


class FeishuMessageFallback:
    """Feishu message delivery with automatic fallback chain."""
    
    def __init__(self, send_func: Callable):
        """
        Initialize with a send function.
        
        Args:
            send_func: Function that takes (content, format) and returns response
        """
        self.send_func = send_func
        self.attempts = []
    
    def _detect_format_error(self, error: Exception, response: Any = None) -> Optional[str]:
        """Detect the type of format error."""
        error_msg = str(error).lower()
        
        # Check error message
        if 'format' in error_msg or 'render' in error_msg or 'markdown' in error_msg:
            return 'markdown_error'
        
        if 'card' in error_msg or 'schema' in error_msg:
            return 'card_error'
        
        # Check response status/message
        if response:
            resp_text = str(response).lower()
            if '400' in resp_text and ('format' in resp_text or 'invalid' in resp_text):
                if 'card' in resp_text:
                    return 'card_error'
                return 'markdown_error'
        
        return None
    
    def _clean_markdown(self, text: str) -> str:
        """Remove problematic markdown."""
        # Remove code blocks that might cause issues
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        
        # Remove complex formatting
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # links
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)  # italic
        
        # Remove images
        text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
        
        return text.strip()
    
    def _to_plain_text(self, content: Any) -> str:
        """Convert content to plain text."""
        if isinstance(content, str):
            return self._clean_markdown(content)
        
        if isinstance(content, dict):
            # Try to extract text from dict
            text = content.get('text', '') or content.get('content', '')
            if text:
                return self._clean_markdown(str(text))
            return self._clean_markdown(json.dumps(content))
        
        return self._clean_markdown(str(content))
    
    def send_with_fallback(self, content: Any, prefer_card: bool = False) -> Dict[str, Any]:
        """
        Send message with automatic fallback chain.
        
        Args:
            content: Message content (str or dict)
            prefer_card: If True, try card first
        
        Returns:
            {'success': bool, 'format': str, 'response': response}
        """
        self.attempts = []
        
        # Strategy 1: Rich text (feishu-post)
        try:
            result = self.send_func(content, 'rich_text')
            self.attempts.append(('rich_text', 'success', result))
            
            # Check if format was rejected
            if hasattr(result, 'status_code'):
                if result.status_code == 400:
                    error_type = self._detect_format_error(Exception("rejected"), result)
                    if error_type:
                        raise Exception(f"Format rejected: {error_type}")
            
            return {'success': True, 'format': 'rich_text', 'response': result}
        except Exception as e:
            self.attempts.append(('rich_text', str(e), None))
            error_type = self._detect_format_error(e)
        
        # Strategy 2: Interactive Card
        if prefer_card:
            try:
                card_content = self._build_card(content)
                result = self.send_func(card_content, 'card')
                self.attempts.append(('card', 'success', result))
                return {'success': True, 'format': 'card', 'response': result}
            except Exception as e:
                self.attempts.append(('card', str(e), None))
        
        # Strategy 3: Plain text (fallback)
        try:
            plain_text = self._to_plain_text(content)
            result = self.send_func(plain_text, 'text')
            self.attempts.append(('text', 'success', result))
            return {'success': True, 'format': 'text', 'response': result}
        except Exception as e:
            self.attempts.append(('text', str(e), None))
            return {'success': False, 'format': 'failed', 'error': str(e)}
    
    def _build_card(self, content: Any) -> Dict:
        """Build a simple Feishu card from content."""
        text = self._to_plain_text(content)
        
        return {
            "config": {
                "wide_screen_mode": True
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": text[:5000]  # Limit length
                }
            ]
        }
    
    def get_attempts(self) -> list:
        """Get list of all attempted formats."""
        return self.attempts


# Demo usage
if __name__ == "__main__":
    # Example usage
    def demo_send(content, format_type):
        print(f"Sending as {format_type}: {content[:50]}...")
        # In real use, call Feishu API here
        return {"status": "ok"}
    
    fallback = FeishuMessageFallback(demo_send)
    
    # Test with markdown content
    test_content = """
# Test Message

This is a **bold** text with `code`.

- Item 1
- Item 2

[Link](https://example.com)
"""
    
    result = fallback.send_with_fallback(test_content)
    print(f"Result: {result}")
    print(f"Attempts: {fallback.get_attempts()}")

"""
Azure Services Integration Module
Provides integration with Azure OpenAI, TTS, STT, and Translator services
"""

import os
import json
from typing import Optional, List
import requests


class AzureOpenAIClient:
    """Client for Azure OpenAI Chat service"""
    
    def __init__(self, endpoint: str, api_key: str, deployment_name: str = "gpt-4"):
        self.endpoint = endpoint.rstrip('/')
        self.api_key = api_key
        self.deployment_name = deployment_name
        self.api_version = "2024-02-15-preview"
        
    def chat_completion(self, messages: List[dict], temperature: float = 0.7) -> str:
        """Send chat completion request to Azure OpenAI"""
        url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        
        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"


class AzureTTSClient:
    """Client for Azure Text-to-Speech service"""
    
    def __init__(self, subscription_key: str, region: str):
        self.subscription_key = subscription_key
        self.region = region
        self.endpoint = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
        
    def synthesize_speech(self, text: str, voice: str = "en-US-JennyNeural", 
                         output_format: str = "audio-16khz-128kbitrate-mono-mp3") -> Optional[bytes]:
        """Convert text to speech"""
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": output_format,
            "User-Agent": "FinancialPlanningApp"
        }
        
        ssml = f"""
        <speak version='1.0' xml:lang='en-US'>
            <voice xml:lang='en-US' name='{voice}'>
                {text}
            </voice>
        </speak>
        """
        
        try:
            response = requests.post(self.endpoint, headers=headers, data=ssml.encode('utf-8'), timeout=30)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"TTS Error: {e}")
            return None


class AzureSTTClient:
    """Client for Azure Speech-to-Text service"""
    
    def __init__(self, subscription_key: str, region: str):
        self.subscription_key = subscription_key
        self.region = region
        self.endpoint = f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
        
    def recognize_from_audio(self, audio_data: bytes, language: str = "en-US") -> str:
        """Convert speech to text"""
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "audio/wav"
        }
        
        params = {
            "language": language,
            "format": "detailed"
        }
        
        try:
            response = requests.post(self.endpoint, headers=headers, params=params, 
                                   data=audio_data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get("RecognitionStatus") == "Success":
                return result.get("DisplayText", "")
            return ""
        except Exception as e:
            print(f"STT Error: {e}")
            return ""


class AzureTranslatorClient:
    """Client for Azure Translator service"""
    
    def __init__(self, subscription_key: str, region: str):
        self.subscription_key = subscription_key
        self.region = region
        self.endpoint = "https://api.cognitive.microsofttranslator.com"
        
    def translate_text(self, text: str, to_language: str, from_language: str = "en") -> str:
        """Translate text to target language"""
        path = '/translate'
        constructed_url = self.endpoint + path
        
        params = {
            'api-version': '3.0',
            'from': from_language,
            'to': to_language
        }
        
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json'
        }
        
        body = [{'text': text}]
        
        try:
            response = requests.post(constructed_url, params=params, headers=headers, 
                                   json=body, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result[0]['translations'][0]['text']
        except Exception as e:
            print(f"Translation Error: {e}")
            return text


class AzureServicesManager:
    """Manager for all Azure services"""
    
    def __init__(self):
        self.chat_client: Optional[AzureOpenAIClient] = None
        self.tts_client: Optional[AzureTTSClient] = None
        self.stt_client: Optional[AzureSTTClient] = None
        self.translator_client: Optional[AzureTranslatorClient] = None
        
    def initialize_from_env(self):
        """Initialize all clients from environment variables"""
        # Azure OpenAI
        openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        openai_key = os.getenv("AZURE_OPENAI_API_KEY")
        openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
        
        if openai_endpoint and openai_key:
            self.chat_client = AzureOpenAIClient(openai_endpoint, openai_key, openai_deployment)
        
        # Azure Speech Services
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")
        
        if speech_key and speech_region:
            self.tts_client = AzureTTSClient(speech_key, speech_region)
            self.stt_client = AzureSTTClient(speech_key, speech_region)
        
        # Azure Translator
        translator_key = os.getenv("AZURE_TRANSLATOR_KEY")
        translator_region = os.getenv("AZURE_TRANSLATOR_REGION")
        
        if translator_key and translator_region:
            self.translator_client = AzureTranslatorClient(translator_key, translator_region)
    
    def initialize_from_config(self, config: dict):
        """Initialize all clients from configuration dictionary"""
        # Azure OpenAI
        if "azure_openai" in config:
            cfg = config["azure_openai"]
            self.chat_client = AzureOpenAIClient(
                cfg.get("endpoint", ""),
                cfg.get("api_key", ""),
                cfg.get("deployment", "gpt-4")
            )
        
        # Azure Speech Services
        if "azure_speech" in config:
            cfg = config["azure_speech"]
            key = cfg.get("key", "")
            region = cfg.get("region", "")
            if key and region:
                self.tts_client = AzureTTSClient(key, region)
                self.stt_client = AzureSTTClient(key, region)
        
        # Azure Translator
        if "azure_translator" in config:
            cfg = config["azure_translator"]
            self.translator_client = AzureTranslatorClient(
                cfg.get("key", ""),
                cfg.get("region", "")
            )

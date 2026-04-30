"""
Supabase Client Module

Manages all database operations for the NeuroLift simulation environment.
Handles CRUD operations for Avatars, Aides, training sessions, and metrics.
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None


class SupabaseClient:
    """
    Singleton client for Supabase database operations.

    Provides methods for managing Avatar, Aide, and training data.
    """

    _instance: Optional['SupabaseClient'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        if not SUPABASE_AVAILABLE:
            self.client = None
            self._initialized = True
            return

        self.supabase_url = os.getenv("VITE_SUPABASE_URL")
        self.supabase_key = os.getenv("VITE_SUPABASE_SUPABASE_ANON_KEY")

        if not self.supabase_url or not self.supabase_key:
            self.client = None
            self._initialized = True
            return

        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        self._initialized = True

    # Avatar Operations

    def create_avatar(self, avatar_id: str, trait_name: str, trait_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Avatar record in the database"""
        if not self.client:
            return None

        data = {
            "avatar_id": avatar_id,
            "trait_name": trait_name,
            "trait_config": trait_config,
            "current_state": "idle",
            "emotional_state": "neutral",
            "cognitive_load": 0.0,
            "stress_level": 0.0,
            "burnout_risk_level": 0.0,
        }

        response = self.client.table("avatars").insert(data).execute()
        return response.data[0] if response.data else None

    def _is_available(self) -> bool:
        """Check if database connection is available"""
        return self.client is not None

    def get_avatar(self, avatar_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an Avatar by avatar_id"""
        if not self._is_available():
            return None

        response = self.client.table("avatars").select("*").eq("avatar_id", avatar_id).maybeSingle().execute()
        return response.data

    def update_avatar_state(self, avatar_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update Avatar state and metrics"""
        if not self._is_available():
            return None

        response = self.client.table("avatars").update(updates).eq("avatar_id", avatar_id).execute()
        return response.data[0] if response.data else None

    def list_avatars(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List all Avatars"""
        if not self._is_available():
            return []

        response = self.client.table("avatars").select("*").limit(limit).execute()
        return response.data

    # Avatar Progress Operations

    def create_avatar_progress(self, avatar_id: str, task_type: str) -> Dict[str, Any]:
        """Create a new progress record for an Avatar task type"""
        if not self._is_available():
            return None

        avatar = self.get_avatar(avatar_id)
        if not avatar:
            return None

        data = {
            "avatar_id": avatar["id"],
            "task_type": task_type,
            "attempts": 0,
            "successes": 0,
            "success_rate": 0.0,
            "independence_level": 0.0,
            "coaching_sessions": 0,
        }

        response = self.client.table("avatar_progress").insert(data).execute()
        return response.data[0] if response.data else None

    def get_avatar_progress(self, avatar_id: str, task_type: str) -> Optional[Dict[str, Any]]:
        """Get progress record for a specific task type"""
        if not self._is_available():
            return None

        avatar = self.get_avatar(avatar_id)
        if not avatar:
            return None

        response = self.client.table("avatar_progress").select("*").eq(
            "avatar_id", avatar["id"]
        ).eq("task_type", task_type).maybeSingle().execute()
        return response.data

    def update_avatar_progress(self, avatar_id: str, task_type: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update progress record"""
        if not self._is_available():
            return None

        avatar = self.get_avatar(avatar_id)
        if not avatar:
            return None

        response = self.client.table("avatar_progress").update(updates).eq(
            "avatar_id", avatar["id"]
        ).eq("task_type", task_type).execute()
        return response.data[0] if response.data else None

    # Aide Operations

    def create_aide(self, aide_id: str, expertise_area: str, expertise_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Aide record"""
        if not self._is_available():
            return None

        data = {
            "aide_id": aide_id,
            "expertise_area": expertise_area,
            "expertise_config": expertise_config,
            "total_interventions": 0,
            "successful_interventions": 0,
            "crisis_interventions": 0,
            "independence_achievements": 0,
        }

        response = self.client.table("aides").insert(data).execute()
        return response.data[0] if response.data else None

    def get_aide(self, aide_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an Aide by aide_id"""
        if not self._is_available():
            return None

        response = self.client.table("aides").select("*").eq("aide_id", aide_id).maybeSingle().execute()
        return response.data

    def update_aide(self, aide_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update Aide metrics"""
        if not self._is_available():
            return None

        response = self.client.table("aides").update(updates).eq("aide_id", aide_id).execute()
        return response.data[0] if response.data else None

    # Training Session Operations

    def create_training_session(self, session_id: str, avatar_id: str, aide_id: str,
                               session_type: str, scenario: str) -> Dict[str, Any]:
        """Create a new training session"""
        if not self._is_available():
            return None

        avatar = self.get_avatar(avatar_id)
        aide = self.get_aide(aide_id)

        if not avatar or not aide:
            return None

        data = {
            "session_id": session_id,
            "avatar_id": avatar["id"],
            "aide_id": aide["id"],
            "session_type": session_type,
            "scenario": scenario,
            "status": "in_progress",
        }

        response = self.client.table("training_sessions").insert(data).execute()
        return response.data[0] if response.data else None

    def get_training_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a training session"""
        if not self._is_available():
            return None

        response = self.client.table("training_sessions").select("*").eq("session_id", session_id).maybeSingle().execute()
        return response.data

    def update_training_session(self, session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a training session"""
        if not self._is_available():
            return None

        response = self.client.table("training_sessions").update(updates).eq("session_id", session_id).execute()
        return response.data[0] if response.data else None

    def end_training_session(self, session_id: str, duration_seconds: int) -> Dict[str, Any]:
        """Mark a training session as completed"""
        updates = {
            "status": "completed",
            "end_time": datetime.now().isoformat(),
            "duration_seconds": duration_seconds,
        }
        return self.update_training_session(session_id, updates)

    # Task Result Operations

    def create_task_result(self, session_id: str, avatar_id: str, task_type: str,
                          success: bool, completion_time: Optional[float], quality_score: float,
                          struggle_indicators: List[str], emotional_state: str,
                          cognitive_load: float, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """Record a task result"""
        if not self._is_available():
            return None

        session = self.get_training_session(session_id)
        avatar = self.get_avatar(avatar_id)

        if not session or not avatar:
            return None

        data = {
            "training_session_id": session["id"],
            "avatar_id": avatar["id"],
            "task_type": task_type,
            "success": success,
            "completion_time_seconds": completion_time,
            "quality_score": quality_score,
            "struggle_indicators": struggle_indicators,
            "emotional_state": emotional_state,
            "cognitive_load": cognitive_load,
            "result_data": result_data,
        }

        response = self.client.table("task_results").insert(data).execute()
        return response.data[0] if response.data else None

    def get_task_results(self, avatar_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent task results for an Avatar"""
        if not self._is_available():
            return []

        avatar = self.get_avatar(avatar_id)
        if not avatar:
            return []

        response = self.client.table("task_results").select("*").eq(
            "avatar_id", avatar["id"]
        ).order("created_at", desc=True).limit(limit).execute()
        return response.data

    # Coaching Action Operations

    def create_coaching_action(self, coaching_id: str, session_id: str, avatar_id: str,
                              aide_id: str, coaching_type: str, urgency: str, strategy: str,
                              techniques: List[str], expected_outcomes: List[str],
                              stress_reduction: float, emotional_boost: float,
                              cognitive_support: float, independence_building: float) -> Dict[str, Any]:
        """Record a coaching action"""
        if not self._is_available():
            return None

        session = self.get_training_session(session_id)
        avatar = self.get_avatar(avatar_id)
        aide = self.get_aide(aide_id)

        if not session or not avatar or not aide:
            return None

        data = {
            "coaching_id": coaching_id,
            "training_session_id": session["id"],
            "avatar_id": avatar["id"],
            "aide_id": aide["id"],
            "coaching_type": coaching_type,
            "urgency": urgency,
            "strategy": strategy,
            "techniques": techniques,
            "expected_outcomes": expected_outcomes,
            "stress_reduction": stress_reduction,
            "emotional_boost": emotional_boost,
            "cognitive_support": cognitive_support,
            "independence_building": independence_building,
        }

        response = self.client.table("coaching_actions").insert(data).execute()
        return response.data[0] if response.data else None

    # Burnout Assessment Operations

    def create_burnout_assessment(self, avatar_id: str, aide_id: str, risk_level: str,
                                 risk_score: float, contributing_factors: List[str],
                                 early_warning_signs: List[str],
                                 intervention_recommendations: List[str],
                                 rrt_activation_needed: bool) -> Dict[str, Any]:
        """Record a burnout assessment"""
        if not self._is_available():
            return None

        avatar = self.get_avatar(avatar_id)
        aide = self.get_aide(aide_id)

        if not avatar or not aide:
            return None

        data = {
            "avatar_id": avatar["id"],
            "aide_id": aide["id"],
            "risk_level": risk_level,
            "risk_score": risk_score,
            "contributing_factors": contributing_factors,
            "early_warning_signs": early_warning_signs,
            "intervention_recommendations": intervention_recommendations,
            "rrt_activation_needed": rrt_activation_needed,
        }

        response = self.client.table("burnout_assessments").insert(data).execute()
        return response.data[0] if response.data else None

    # Metrics Operations

    def record_metric(self, metric_type: str, metric_value: float, avatar_id: Optional[str] = None,
                     aide_id: Optional[str] = None, metric_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Record a metric"""
        if not self._is_available():
            return None

        avatar_db_id = None
        aide_db_id = None

        if avatar_id:
            avatar = self.get_avatar(avatar_id)
            if avatar:
                avatar_db_id = avatar["id"]

        if aide_id:
            aide = self.get_aide(aide_id)
            if aide:
                aide_db_id = aide["id"]

        data = {
            "avatar_id": avatar_db_id,
            "aide_id": aide_db_id,
            "metric_type": metric_type,
            "metric_value": metric_value,
            "metric_data": metric_data or {},
        }

        response = self.client.table("metrics").insert(data).execute()
        return response.data[0] if response.data else None

    def get_metrics(self, metric_type: str, avatar_id: Optional[str] = None,
                   limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve metrics by type"""
        if not self._is_available():
            return []

        query = self.client.table("metrics").select("*").eq("metric_type", metric_type)

        if avatar_id:
            avatar = self.get_avatar(avatar_id)
            if avatar:
                query = query.eq("avatar_id", avatar["id"])

        response = query.order("created_at", desc=True).limit(limit).execute()
        return response.data

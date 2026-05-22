"""
Attention Deficit Trait Implementation

Implements the sustained attention deficit trait for StayAlert Avatar.
This trait simulates authentic struggles with maintaining focus on tasks,
especially those that are repetitive or not immediately engaging.
"""

import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from ..base_avatar import BaseAvatar


class AttentionDeficit(BaseAvatar):
    """
    Avatar with sustained attention deficit trait.
    
    This Avatar struggles to maintain focus on tasks, especially those that are
    repetitive, boring, or not immediately engaging. They experience authentic
    attention lapses, distraction sensitivity, and mental fatigue.
    """
    
    def __init__(self, avatar_id: str, trait_config: Dict[str, Any]):
        super().__init__(avatar_id, trait_config)
        
        # Attention-specific state
        self.current_attention_span = trait_config.get("attention_span_base", 5.0)
        self.distraction_sensitivity = trait_config.get("distraction_sensitivity", 0.8)
        self.task_engagement_threshold = trait_config.get("task_engagement_threshold", 0.6)
        self.focus_recovery_time = trait_config.get("focus_recovery_time", 30.0)
        self.hyperfocus_probability = trait_config.get("hyperfocus_probability", 0.1)
        self.hyperfocus_duration = trait_config.get("hyperfocus_duration", 120.0)
        
        # Dynamic attention state
        self.current_focus_level = 0.7
        self.distraction_level = 0.3
        self.mental_fatigue = 0.0
        self.last_focus_loss: Optional[datetime] = None
        self.hyperfocus_active = False
        self.hyperfocus_start_time: Optional[datetime] = None
        
    def get_adhd_trait_impact(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate how attention deficit affects task performance.
        
        Args:
            task_context: Context about the current task and environment
            
        Returns:
            Dictionary with trait impact details
        """
        # Calculate task engagement level
        task_engagement = self._calculate_task_engagement(task_context)
        
        # Determine if hyperfocus is active
        if self._check_hyperfocus_activation(task_context):
            self._activate_hyperfocus()
        
        # Calculate attention impact
        attention_impact = self._calculate_attention_impact(task_context, task_engagement)
        
        # Calculate difficulty modifier
        difficulty_modifier = self._calculate_difficulty_modifier(attention_impact, task_engagement)
        
        # Calculate quality modifier
        quality_modifier = self._calculate_quality_modifier(attention_impact)
        
        # Calculate time modifier
        time_modifier = self._calculate_time_modifier(attention_impact)
        
        # Calculate cognitive load modifier
        cognitive_load_modifier = self._calculate_cognitive_load_modifier(attention_impact)
        
        return {
            "difficulty_modifier": difficulty_modifier,
            "struggle_indicators": self._generate_struggle_indicators(attention_impact),
            "quality_modifier": quality_modifier,
            "time_modifier": time_modifier,
            "cognitive_load_modifier": cognitive_load_modifier,
            "attention_impact": attention_impact,
            "task_engagement": task_engagement,
            "hyperfocus_active": self.hyperfocus_active,
        }
    
    def simulate_struggle(self, task_context: Dict[str, Any]) -> List[str]:
        """
        Simulate authentic attention deficit struggles.
        
        Args:
            task_context: Context about the current task
            
        Returns:
            List of struggle indicators
        """
        struggles = []
        
        # Check for attention lapses
        if self._should_lose_focus(task_context):
            struggles.append("attention_lapse")
            self._lose_focus()
        
        # Check for distractions
        if self._should_get_distracted(task_context):
            struggles.append("environmental_distraction")
            self._increase_distraction()
        
        # Check for mental fatigue
        if self._should_experience_fatigue(task_context):
            struggles.append("mental_fatigue")
            self._increase_fatigue()
        
        # Check for task disengagement
        if self._should_disengage_from_task(task_context):
            struggles.append("task_disengagement")
            self._disengage_from_task()
        
        # Check for focus recovery struggles
        if self._should_struggle_with_recovery():
            struggles.append("focus_recovery_difficulty")
        
        return struggles
    
    def _calculate_task_engagement(self, task_context: Dict[str, Any]) -> float:
        """Calculate how engaging the current task is"""
        # Base engagement from task properties
        base_engagement = task_context.get("task_engagement", 0.5)
        
        # Adjust for task type
        task_type = task_context.get("task_type", "unknown")
        if task_type in ["creative", "problem_solving", "interactive"]:
            base_engagement += 0.2
        elif task_type in ["repetitive", "data_entry", "routine"]:
            base_engagement -= 0.3
        
        # Adjust for novelty
        novelty = task_context.get("novelty", 0.5)
        base_engagement += (novelty - 0.5) * 0.3
        
        # Adjust for immediate rewards
        immediate_rewards = task_context.get("immediate_rewards", 0.0)
        base_engagement += immediate_rewards * 0.4
        
        return max(0.0, min(1.0, base_engagement))
    
    def _check_hyperfocus_activation(self, task_context: Dict[str, Any]) -> bool:
        """Check if hyperfocus should be activated"""
        if self.hyperfocus_active:
            return False
        
        # Check if task is highly engaging
        task_engagement = self._calculate_task_engagement(task_context)
        if task_engagement > 0.8:
            return random.random() < self.hyperfocus_probability
        
        return False
    
    def _activate_hyperfocus(self) -> None:
        """Activate hyperfocus state"""
        self.hyperfocus_active = True
        self.hyperfocus_start_time = datetime.now()
        self.current_focus_level = 1.0
        self.distraction_level = 0.0
        self.mental_fatigue = 0.0
    
    def _calculate_attention_impact(self, task_context: Dict[str, Any], 
                                  task_engagement: float) -> Dict[str, Any]:
        """Calculate the impact of attention deficit on current task"""
        # Base attention capacity
        base_attention = self.current_attention_span
        
        # Adjust for current focus level
        effective_attention = base_attention * self.current_focus_level
        
        # Adjust for distraction level
        effective_attention *= (1.0 - self.distraction_level)
        
        # Adjust for mental fatigue
        effective_attention *= (1.0 - self.mental_fatigue)
        
        # Adjust for task engagement
        if task_engagement < self.task_engagement_threshold:
            effective_attention *= 0.5
        
        # Hyperfocus bonus
        if self.hyperfocus_active:
            effective_attention *= 2.0
        
        return {
            "effective_attention": effective_attention,
            "focus_level": self.current_focus_level,
            "distraction_level": self.distraction_level,
            "mental_fatigue": self.mental_fatigue,
            "task_engagement": task_engagement,
        }
    
    def _calculate_difficulty_modifier(self, attention_impact: Dict[str, Any], 
                                     task_engagement: float) -> float:
        """Calculate how much attention deficit increases task difficulty"""
        effective_attention = attention_impact["effective_attention"]
        
        # Base difficulty modifier
        base_modifier = 1.0
        
        # Increase difficulty for low attention
        if effective_attention < 3.0:
            base_modifier += 0.5
        elif effective_attention < 5.0:
            base_modifier += 0.3
        
        # Increase difficulty for low engagement
        if task_engagement < 0.3:
            base_modifier += 0.4
        elif task_engagement < 0.5:
            base_modifier += 0.2
        
        # Reduce difficulty during hyperfocus
        if self.hyperfocus_active:
            base_modifier *= 0.7
        
        return base_modifier
    
    def _calculate_quality_modifier(self, attention_impact: Dict[str, Any]) -> float:
        """Calculate quality reduction due to attention issues"""
        effective_attention = attention_impact["effective_attention"]
        
        if effective_attention < 2.0:
            return 0.4
        elif effective_attention < 4.0:
            return 0.2
        elif effective_attention < 6.0:
            return 0.1
        else:
            return 0.0
    
    def _calculate_time_modifier(self, attention_impact: Dict[str, Any]) -> float:
        """Calculate time increase due to attention issues"""
        effective_attention = attention_impact["effective_attention"]
        
        if effective_attention < 3.0:
            return 2.0
        elif effective_attention < 5.0:
            return 1.5
        else:
            return 1.0
    
    def _calculate_cognitive_load_modifier(self, attention_impact: Dict[str, Any]) -> float:
        """Calculate cognitive load increase due to attention issues"""
        # Higher cognitive load when struggling with attention
        return self.distraction_level + self.mental_fatigue
    
    def _generate_struggle_indicators(self, attention_impact: Dict[str, Any]) -> List[str]:
        """Generate specific struggle indicators based on attention impact"""
        indicators = []
        
        if attention_impact["focus_level"] < 0.5:
            indicators.append("low_focus_level")
        
        if attention_impact["distraction_level"] > 0.6:
            indicators.append("high_distraction")
        
        if attention_impact["mental_fatigue"] > 0.7:
            indicators.append("mental_exhaustion")
        
        if attention_impact["task_engagement"] < 0.3:
            indicators.append("low_task_engagement")
        
        return indicators
    
    def _should_lose_focus(self, task_context: Dict[str, Any]) -> bool:
        """Determine if Avatar should lose focus"""
        # Higher probability with low engagement
        task_engagement = self._calculate_task_engagement(task_context)
        if task_engagement < 0.4:
            return random.random() < 0.6
        elif task_engagement < 0.6:
            return random.random() < 0.3
        else:
            return random.random() < 0.1
    
    def _lose_focus(self) -> None:
        """Simulate losing focus"""
        self.current_focus_level = max(0.2, self.current_focus_level - 0.3)
        self.last_focus_loss = datetime.now()
    
    def _should_get_distracted(self, task_context: Dict[str, Any]) -> bool:
        """Determine if Avatar should get distracted"""
        # Higher probability with high distraction sensitivity
        base_probability = self.distraction_sensitivity * 0.3
        
        # Increase probability with low focus
        if self.current_focus_level < 0.5:
            base_probability += 0.2
        
        return random.random() < base_probability
    
    def _increase_distraction(self) -> None:
        """Simulate increased distraction"""
        self.distraction_level = min(1.0, self.distraction_level + 0.2)
    
    def _should_experience_fatigue(self, task_context: Dict[str, Any]) -> bool:
        """Determine if Avatar should experience mental fatigue"""
        # Higher probability with sustained effort
        task_duration = task_context.get("expected_duration_minutes", 10)
        if task_duration > 20:
            return random.random() < 0.4
        elif task_duration > 10:
            return random.random() < 0.2
        else:
            return random.random() < 0.1
    
    def _increase_fatigue(self) -> None:
        """Simulate increased mental fatigue"""
        self.mental_fatigue = min(1.0, self.mental_fatigue + 0.15)
    
    def _should_disengage_from_task(self, task_context: Dict[str, Any]) -> bool:
        """Determine if Avatar should disengage from task"""
        task_engagement = self._calculate_task_engagement(task_context)
        if task_engagement < 0.3 and self.current_focus_level < 0.4:
            return random.random() < 0.5
        return False
    
    def _disengage_from_task(self) -> None:
        """Simulate task disengagement"""
        self.current_focus_level = max(0.1, self.current_focus_level - 0.4)
        self.distraction_level = min(1.0, self.distraction_level + 0.3)
    
    def _should_struggle_with_recovery(self) -> bool:
        """Determine if Avatar should struggle with focus recovery"""
        if self.last_focus_loss is None:
            return False
        
        time_since_loss = (datetime.now() - self.last_focus_loss).total_seconds()
        recovery_threshold = self.focus_recovery_time
        
        if time_since_loss > recovery_threshold:
            return random.random() < 0.3
        
        return False
    
    def update_attention_state(self) -> None:
        """Update attention state over time"""
        # Check hyperfocus duration
        if self.hyperfocus_active and self.hyperfocus_start_time:
            duration = (datetime.now() - self.hyperfocus_start_time).total_seconds()
            if duration > self.hyperfocus_duration:
                self._end_hyperfocus()
        
        # Gradual focus recovery
        if not self.hyperfocus_active:
            self.current_focus_level = min(1.0, self.current_focus_level + 0.05)
        
        # Gradual distraction reduction
        self.distraction_level = max(0.0, self.distraction_level - 0.02)
        
        # Gradual fatigue reduction
        self.mental_fatigue = max(0.0, self.mental_fatigue - 0.01)
    
    def _end_hyperfocus(self) -> None:
        """End hyperfocus state"""
        self.hyperfocus_active = False
        self.hyperfocus_start_time = None
        self.current_focus_level = 0.6  # Post-hyperfocus dip
        self.mental_fatigue = 0.8  # Hyperfocus exhaustion
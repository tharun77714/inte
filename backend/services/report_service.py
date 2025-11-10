"""
Report generation service for personalized improvement reports
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ReportService:
    """Service for generating personalized improvement reports"""
    
    async def generate_report(self, session_data: Dict[str, Any], domain: str) -> Dict:
        """
        Generate comprehensive improvement report
        
        Args:
            session_data: Complete session data with questions, answers, and feedback
            domain: Interview domain
        
        Returns:
            Detailed report dictionary
        """
        try:
            # Extract data
            questions = session_data.get("questions", [])
            answers = session_data.get("answers", [])
            feedback_history = session_data.get("feedback_history", [])
            
            # Calculate overall statistics
            stats = self._calculate_statistics(feedback_history)
            
            # Identify strengths and weaknesses
            strengths = self._identify_strengths(feedback_history)
            weaknesses = self._identify_weaknesses(feedback_history)
            
            # Generate improvement plan
            improvement_plan = self._generate_improvement_plan(
                weaknesses, domain, stats
            )
            
            # Create report
            report = {
                "session_id": session_data.get("session_id"),
                "domain": domain,
                "date": datetime.now().isoformat(),
                "summary": {
                    "total_questions": len(questions),
                    "overall_score": stats["overall_score"],
                    "communication_score": stats["avg_communication"],
                    "technical_score": stats["avg_technical"]
                },
                "statistics": stats,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "improvement_plan": improvement_plan,
                "detailed_feedback": feedback_history,
                "recommendations": self._generate_recommendations(domain, stats)
            }
            
            return report
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {
                "error": str(e),
                "message": "Report generation failed"
            }
    
    def _calculate_statistics(self, feedback_history: List[Dict]) -> Dict:
        """Calculate statistics from feedback history"""
        if not feedback_history:
            return {
                "overall_score": 0.0,
                "avg_communication": 0.0,
                "avg_technical": 0.0,
                "total_filler_words": 0,
                "avg_clarity": 0.0
            }
        
        comm_scores = [f.get("communication", {}).get("score", 0.0) for f in feedback_history]
        tech_scores = [f.get("technical", {}).get("score", 0.0) for f in feedback_history]
        overall_scores = [f.get("overall_score", 0.0) for f in feedback_history]
        
        total_fillers = sum(
            f.get("communication", {}).get("filler_words_count", 0)
            for f in feedback_history
        )
        
        clarity_scores = [
            f.get("communication", {}).get("clarity_score", 0.0)
            for f in feedback_history
        ]
        
        return {
            "overall_score": round(sum(overall_scores) / len(overall_scores), 2) if overall_scores else 0.0,
            "avg_communication": round(sum(comm_scores) / len(comm_scores), 2) if comm_scores else 0.0,
            "avg_technical": round(sum(tech_scores) / len(tech_scores), 2) if tech_scores else 0.0,
            "total_filler_words": total_fillers,
            "avg_clarity": round(sum(clarity_scores) / len(clarity_scores), 2) if clarity_scores else 0.0,
            "sessions_completed": len(feedback_history)
        }
    
    def _identify_strengths(self, feedback_history: List[Dict]) -> List[str]:
        """Identify candidate strengths"""
        strengths = []
        
        if not feedback_history:
            return ["No data available"]
        
        # Check communication
        avg_comm = sum(
            f.get("communication", {}).get("score", 0.0)
            for f in feedback_history
        ) / len(feedback_history)
        
        if avg_comm >= 0.7:
            strengths.append("Strong communication skills")
        elif avg_comm >= 0.6:
            strengths.append("Good communication foundation")
        
        # Check technical
        avg_tech = sum(
            f.get("technical", {}).get("score", 0.0)
            for f in feedback_history
        ) / len(feedback_history)
        
        if avg_tech >= 0.7:
            strengths.append("Solid technical knowledge")
        elif avg_tech >= 0.6:
            strengths.append("Good technical understanding")
        
        # Check filler words
        avg_fillers = sum(
            f.get("communication", {}).get("filler_words_count", 0)
            for f in feedback_history
        ) / len(feedback_history)
        
        if avg_fillers < 3:
            strengths.append("Minimal use of filler words")
        
        # Check clarity
        avg_clarity = sum(
            f.get("communication", {}).get("clarity_score", 0.0)
            for f in feedback_history
        ) / len(feedback_history)
        
        if avg_clarity >= 0.7:
            strengths.append("Clear and articulate responses")
        
        if not strengths:
            strengths.append("Shows potential with practice")
        
        return strengths
    
    def _identify_weaknesses(self, feedback_history: List[Dict]) -> List[str]:
        """Identify areas for improvement"""
        weaknesses = []
        
        if not feedback_history:
            return ["Complete more sessions for analysis"]
        
        # Check communication
        avg_comm = sum(
            f.get("communication", {}).get("score", 0.0)
            for f in feedback_history
        ) / len(feedback_history)
        
        if avg_comm < 0.6:
            weaknesses.append("Communication skills need improvement")
        
        # Check technical
        avg_tech = sum(
            f.get("technical", {}).get("score", 0.0)
            for f in feedback_history
        ) / len(feedback_history)
        
        if avg_tech < 0.6:
            weaknesses.append("Technical knowledge needs strengthening")
        
        # Check filler words
        avg_fillers = sum(
            f.get("communication", {}).get("filler_words_count", 0)
            for f in feedback_history
        ) / len(feedback_history)
        
        if avg_fillers > 5:
            weaknesses.append(f"High use of filler words (average: {avg_fillers:.1f})")
        
        # Check clarity
        avg_clarity = sum(
            f.get("communication", {}).get("clarity_score", 0.0)
            for f in feedback_history
        ) / len(feedback_history)
        
        if avg_clarity < 0.6:
            weaknesses.append("Response clarity needs improvement")
        
        if not weaknesses:
            weaknesses.append("Continue practicing to maintain performance")
        
        return weaknesses
    
    def _generate_improvement_plan(
        self,
        weaknesses: List[str],
        domain: str,
        stats: Dict
    ) -> List[Dict]:
        """Generate actionable improvement plan"""
        plan = []
        
        # Communication improvements
        if stats["avg_communication"] < 0.7:
            plan.append({
                "area": "Communication",
                "priority": "High",
                "actions": [
                    "Practice speaking out loud daily",
                    "Record yourself answering questions",
                    "Focus on reducing filler words",
                    "Work on sentence structure and clarity"
                ],
                "resources": [
                    "Join public speaking groups",
                    "Practice with mock interviews",
                    "Use voice recording apps for self-review"
                ]
            })
        
        # Technical improvements
        if stats["avg_technical"] < 0.7:
            plan.append({
                "area": "Technical Knowledge",
                "priority": "High",
                "actions": [
                    f"Review fundamental concepts in {domain}",
                    "Practice explaining technical concepts simply",
                    "Work on coding problems (if applicable)",
                    "Study common interview questions for your domain"
                ],
                "resources": [
                    "Online courses and tutorials",
                    "Technical blogs and documentation",
                    "Practice platforms (LeetCode, HackerRank, etc.)"
                ]
            })
        
        # Filler words
        if stats["total_filler_words"] > 10:
            plan.append({
                "area": "Filler Words",
                "priority": "Medium",
                "actions": [
                    "Practice pausing instead of using filler words",
                    "Slow down your speech slightly",
                    "Think before speaking",
                    "Use silence as a tool, not filler words"
                ],
                "resources": [
                    "Speech therapy techniques",
                    "Mindfulness and breathing exercises"
                ]
            })
        
        if not plan:
            plan.append({
                "area": "Maintenance",
                "priority": "Low",
                "actions": [
                    "Continue regular practice",
                    "Maintain consistency in performance",
                    "Challenge yourself with harder questions"
                ],
                "resources": []
            })
        
        return plan
    
    def _generate_recommendations(self, domain: str, stats: Dict) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        if stats["overall_score"] >= 0.7:
            recommendations.append(
                "Excellent performance! You're well-prepared for interviews."
            )
            recommendations.append(
                "Continue practicing to maintain your skills and confidence."
            )
        elif stats["overall_score"] >= 0.5:
            recommendations.append(
                "You're making good progress. Focus on identified weak areas."
            )
            recommendations.append(
                "Practice more frequently to build consistency."
            )
        else:
            recommendations.append(
                "Focus on fundamentals before moving to advanced topics."
            )
            recommendations.append(
                "Consider structured learning programs for your domain."
            )
        
        recommendations.append(
            f"Practice {domain} specific questions regularly."
        )
        recommendations.append(
            "Record your practice sessions and review them critically."
        )
        
        return recommendations


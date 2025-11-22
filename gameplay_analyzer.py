"""
LoL Gameplay Analyzer - Système d'analyse IA de replays
Analyse les performances d'un joueur et fournit des conseils personnalisés
"""

import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GameMetrics:
    """Métriques d'une partie"""
    game_duration: int  # en secondes
    champion: str
    role: str
    
    # CS & Farm
    total_cs: int
    cs_per_min: float
    jungle_cs: int
    
    # Combat
    kills: int
    deaths: int
    assists: int
    kda: float
    damage_dealt: int
    damage_taken: int
    damage_per_min: float
    
    # Vision
    vision_score: int
    wards_placed: int
    wards_destroyed: int
    control_wards_bought: int
    
    # Objectifs
    turret_plates: int
    turrets_destroyed: int
    dragons_secured: int
    barons_secured: int
    objective_participation: float  # % d'objectifs auxquels on a participé
    
    # Or
    gold_earned: int
    gold_per_min: float
    
    # Temps
    time_cc_others: float
    time_spent_dead: int
    
    # Contexte équipe
    team_average_kda: float  # KDA moyen des alliés
    nemesis_champion: str  # Champion qui vous a le plus tué


@dataclass
class TimelineEvent:
    """Événement dans la timeline"""
    timestamp: int  # en secondes
    event_type: str  # "death", "kill", "objective", "recall", etc.
    position: Optional[Tuple[int, int]]
    description: str
    severity: str  # "critical", "warning", "info"


class GameplayAnalyzer:
    """Analyseur de gameplay avec IA"""
    
    def __init__(self):
        self.benchmarks = self.load_benchmarks()
        
    def load_benchmarks(self) -> Dict:
        """Charge les benchmarks de performance par rôle et elo"""
        # Benchmarks moyens pour chaque rôle (base Iron-Gold)
        return {
            "Top": {
                "cs_per_min": 6.5,
                "vision_score_per_min": 1.2,
                "damage_per_min": 600,
                "kda_target": 2.5
            },
            "Jungle": {
                "cs_per_min": 5.0,
                "vision_score_per_min": 1.5,
                "damage_per_min": 500,
                "kda_target": 2.8
            },
            "Mid": {
                "cs_per_min": 7.0,
                "vision_score_per_min": 1.0,
                "damage_per_min": 700,
                "kda_target": 2.6
            },
            "ADC": {
                "cs_per_min": 7.5,
                "vision_score_per_min": 0.8,
                "damage_per_min": 800,
                "kda_target": 3.0
            },
            "Support": {
                "cs_per_min": 1.5,
                "vision_score_per_min": 2.5,
                "damage_per_min": 300,
                "kda_target": 3.5
            }
        }
    
    def analyze_game(self, metrics: GameMetrics, timeline: List[TimelineEvent] = None) -> Dict:
        """Analyse complète d'une partie"""
        
        analysis = {
            "overall_score": 0,
            "strengths": [],
            "weaknesses": [],
            "critical_issues": [],
            "recommendations": [],
            "timeline_analysis": [],
            "category_scores": {}
        }
        
        # Analyses par catégorie
        cs_analysis = self.analyze_cs(metrics)
        combat_analysis = self.analyze_combat(metrics)
        vision_analysis = self.analyze_vision(metrics)
        objective_analysis = self.analyze_objectives(metrics)
        positioning_analysis = self.analyze_positioning(metrics, timeline)
        
        # Compilation des résultats
        all_analyses = [cs_analysis, combat_analysis, vision_analysis, 
                       objective_analysis, positioning_analysis]
        
        for cat_analysis in all_analyses:
            analysis["category_scores"][cat_analysis["category"]] = cat_analysis["score"]
            analysis["strengths"].extend(cat_analysis.get("strengths", []))
            analysis["weaknesses"].extend(cat_analysis.get("weaknesses", []))
            analysis["critical_issues"].extend(cat_analysis.get("critical", []))
            analysis["recommendations"].extend(cat_analysis.get("recommendations", []))
        
        # Calcul du score global
        analysis["overall_score"] = sum(analysis["category_scores"].values()) / len(analysis["category_scores"])
        
        # Analyse de la timeline si disponible
        if timeline:
            analysis["timeline_analysis"] = self.analyze_timeline(timeline, metrics)
        
        return analysis
    
    def analyze_cs(self, metrics: GameMetrics) -> Dict:
        """Analyse du farm et CS"""
        benchmark = self.benchmarks.get(metrics.role, {})
        target_cs_per_min = benchmark.get("cs_per_min", 6.0)
        
        game_duration_min = metrics.game_duration / 60
        expected_cs = target_cs_per_min * game_duration_min
        cs_efficiency = (metrics.total_cs / expected_cs) * 100 if expected_cs > 0 else 0
        
        analysis = {
            "category": "Farm & CS",
            "score": min(cs_efficiency, 100),
            "strengths": [],
            "weaknesses": [],
            "critical": [],
            "recommendations": []
        }
        
        # Évaluation
        if cs_efficiency >= 90:
            analysis["strengths"].append(f"Excellent farm: {metrics.cs_per_min:.1f} CS/min (top tier)")
            analysis["score"] = 100
        elif cs_efficiency >= 75:
            analysis["strengths"].append(f"Bon farm: {metrics.cs_per_min:.1f} CS/min")
            analysis["score"] = 85
        elif cs_efficiency >= 60:
            analysis["weaknesses"].append(f"Farm moyen: {metrics.cs_per_min:.1f} CS/min (objectif: {target_cs_per_min:.1f})")
            analysis["recommendations"].append("Pratique le last-hit en practice tool 10 min/jour")
            analysis["score"] = 60
        else:
            analysis["critical"].append(f"Farm très faible: {metrics.cs_per_min:.1f} CS/min")
            analysis["recommendations"].append("PRIORITÉ: Améliorer le farm - objectif minimum 6 CS/min")
            analysis["recommendations"].append("Utilise le practice tool pour t'entraîner au last-hit")
            analysis["score"] = 40
        
        # Analyse par phase de jeu
        if metrics.game_duration > 2100:  # > 35 minutes
            if metrics.total_cs < (7 * 35):  # Moins de 7 CS/min à 35min
                analysis["critical"].append("CS très faible en late game (35+ min)")
                analysis["recommendations"].append("Ne néglige pas les side lanes en late game")
        
        return analysis
    
    def analyze_combat(self, metrics: GameMetrics) -> Dict:
        """Analyse des combats et KDA"""
        benchmark = self.benchmarks.get(metrics.role, {})
        target_kda = benchmark.get("kda_target", 2.5)
        target_dpm = benchmark.get("damage_per_min", 600)
        
        analysis = {
            "category": "Combat & Impact",
            "score": 50,
            "strengths": [],
            "weaknesses": [],
            "critical": [],
            "recommendations": []
        }
        
        # Contexte d'équipe: compare ton KDA avec celui de tes alliés
        team_kda = metrics.team_average_kda
        kda_vs_team = (metrics.kda / team_kda) if team_kda > 0 else 1.0
        
        if kda_vs_team >= 1.3:
            analysis["strengths"].append(f"Tu portes ton équipe! KDA: {metrics.kda:.2f} vs équipe: {team_kda:.2f}")
            analysis["score"] += 15
        elif kda_vs_team <= 0.7:
            analysis["critical"].append(f"Tu sous-perforces par rapport à ton équipe (KDA: {metrics.kda:.2f} vs {team_kda:.2f})")
            analysis["recommendations"].append("Ton équipe joue mieux que toi - adapte ton style de jeu")
            analysis["score"] -= 15
        
        # Analyse KDA
        if metrics.kda >= target_kda * 1.5:
            analysis["strengths"].append(f"Excellent KDA: {metrics.kda:.2f} (très peu de morts)")
            analysis["score"] += 25
        elif metrics.kda >= target_kda:
            analysis["strengths"].append(f"Bon KDA: {metrics.kda:.2f}")
            analysis["score"] += 15
        elif metrics.kda >= target_kda * 0.7:
            analysis["weaknesses"].append(f"KDA moyen: {metrics.kda:.2f} (objectif: {target_kda:.1f})")
            analysis["score"] += 5
        else:
            analysis["critical"].append(f"KDA très faible: {metrics.kda:.2f}")
            analysis["recommendations"].append("Trop de morts - focus sur le positionnement")
            analysis["score"] -= 10
        
        # Analyse des morts
        game_duration_min = metrics.game_duration / 60
        deaths_per_min = metrics.deaths / game_duration_min
        
        if deaths_per_min > 0.25:  # Plus d'1 mort toutes les 4 minutes
            analysis["critical"].append(f"Trop de morts: {metrics.deaths} ({deaths_per_min:.2f}/min)")
            analysis["recommendations"].append("Analyse tes morts: mauvais trades? overextend? pas de vision?")
            analysis["recommendations"].append("Regarde la minimap toutes les 3-5 secondes")
        
        # Analyse du champion nemesis
        if metrics.nemesis_champion and metrics.nemesis_champion != "Aucun":
            analysis["critical"].append(f"Champion problématique: {metrics.nemesis_champion} te tue souvent")
            analysis["recommendations"].append(f"Étudie le matchup contre {metrics.nemesis_champion}")
            analysis["recommendations"].append(f"Build défensif contre {metrics.nemesis_champion} (Zhonya's, Banshee's, etc.)")
            analysis["recommendations"].append(f"Demande de l'aide à ton jungler pour gérer {metrics.nemesis_champion}")
        
        # Analyse des dégâts
        dpm_ratio = metrics.damage_per_min / target_dpm
        
        if dpm_ratio >= 1.2:
            analysis["strengths"].append(f"Excellent impact damage: {metrics.damage_per_min:.0f} DPM")
            analysis["score"] += 25
        elif dpm_ratio >= 0.9:
            analysis["strengths"].append(f"Bon impact damage: {metrics.damage_per_min:.0f} DPM")
            analysis["score"] += 15
        elif dpm_ratio >= 0.7:
            analysis["weaknesses"].append(f"Impact damage moyen: {metrics.damage_per_min:.0f} DPM")
            analysis["score"] += 5
        else:
            analysis["critical"].append(f"Impact damage très faible: {metrics.damage_per_min:.0f} DPM")
            analysis["recommendations"].append("Participe plus aux combats et teamfights")
        
        return analysis
    
    def analyze_vision(self, metrics: GameMetrics) -> Dict:
        """Analyse de la vision"""
        benchmark = self.benchmarks.get(metrics.role, {})
        target_vision_per_min = benchmark.get("vision_score_per_min", 1.5)
        
        game_duration_min = metrics.game_duration / 60
        vision_per_min = metrics.vision_score / game_duration_min
        
        analysis = {
            "category": "Vision & Map Control",
            "score": 50,
            "strengths": [],
            "weaknesses": [],
            "critical": [],
            "recommendations": []
        }
        
        vision_ratio = vision_per_min / target_vision_per_min
        
        if vision_ratio >= 1.2:
            analysis["strengths"].append(f"Excellente vision: {vision_per_min:.1f} score/min")
            analysis["score"] = 100
        elif vision_ratio >= 0.9:
            analysis["strengths"].append(f"Bonne vision: {vision_per_min:.1f} score/min")
            analysis["score"] = 80
        elif vision_ratio >= 0.6:
            analysis["weaknesses"].append(f"Vision moyenne: {vision_per_min:.1f} score/min")
            analysis["recommendations"].append("Place plus de wards dans les zones clés (objectives, jungle ennemie)")
            analysis["score"] = 60
        else:
            analysis["critical"].append(f"Vision très faible: {vision_per_min:.1f} score/min")
            analysis["recommendations"].append("PRIORITÉ: Achète et place plus de control wards")
            analysis["recommendations"].append("Utilise ton trinket dès qu'elle est disponible")
            analysis["score"] = 30
        
        # Analyse des control wards
        expected_control_wards = game_duration_min * 0.3  # ~1 toutes les 3 min
        if metrics.control_wards_bought < expected_control_wards * 0.5:
            analysis["critical"].append(f"Très peu de control wards achetés: {metrics.control_wards_bought}")
            analysis["recommendations"].append("Achète au moins 1 control ward à chaque recall")
        
        return analysis
    
    def analyze_objectives(self, metrics: GameMetrics) -> Dict:
        """Analyse de la prise d'objectifs"""
        analysis = {
            "category": "Objectifs & Map Pressure",
            "score": 50,
            "strengths": [],
            "weaknesses": [],
            "critical": [],
            "recommendations": []
        }
        
        total_objectives = (metrics.turrets_destroyed + 
                          metrics.dragons_secured + 
                          metrics.barons_secured * 2)
        
        # Analyse de la participation aux objectifs
        if metrics.objective_participation >= 70:
            analysis["strengths"].append(f"Excellente participation aux objectifs: {metrics.objective_participation:.0f}%")
            analysis["score"] = 90
        elif metrics.objective_participation >= 50:
            analysis["strengths"].append(f"Bonne participation aux objectifs: {metrics.objective_participation:.0f}%")
            analysis["score"] = 75
        elif metrics.objective_participation >= 30:
            analysis["weaknesses"].append(f"Participation moyenne aux objectifs: {metrics.objective_participation:.0f}%")
            analysis["recommendations"].append("Sois plus présent lors des prises de dragons et barons")
            analysis["score"] = 60
        else:
            analysis["critical"].append(f"Très faible participation aux objectifs: {metrics.objective_participation:.0f}%")
            analysis["recommendations"].append("PRIORITÉ: Rotate vers les objectifs avec ton équipe")
            analysis["score"] = 40
        
        # Analyse des tours détruites
        if metrics.turrets_destroyed >= 5:
            analysis["strengths"].append(f"Excellente destruction de tours: {metrics.turrets_destroyed}")
        elif metrics.turrets_destroyed >= 3:
            analysis["strengths"].append(f"Bonne destruction de tours: {metrics.turrets_destroyed}")
        elif metrics.turrets_destroyed <= 1:
            analysis["weaknesses"].append(f"Peu de tours détruites: {metrics.turrets_destroyed}")
            analysis["recommendations"].append("Push les side lanes pour prendre des tours")
        
        # Analyse spécifique des turret plates
        if metrics.turret_plates < 2 and metrics.role in ["Top", "Mid", "ADC"]:
            analysis["weaknesses"].append("Peu de turret plates prises")
            analysis["recommendations"].append("Poke la tour pour prendre des plates en early game (avant 14min)")
        
        # Contexte: comparaison avec l'équipe
        if total_objectives < 3 and metrics.objective_participation < 40:
            analysis["critical"].append("Très peu impliqué dans les objectifs majeurs")
            analysis["recommendations"].append("Ward autour des objectifs et spam-ping pour que ton équipe rotate")
        
        return analysis
    
    def analyze_positioning(self, metrics: GameMetrics, 
                          timeline: List[TimelineEvent] = None) -> Dict:
        """Analyse du positionnement et des décisions"""
        analysis = {
            "category": "Positionnement & Décisions",
            "score": 70,
            "strengths": [],
            "weaknesses": [],
            "critical": [],
            "recommendations": []
        }
        
        if not timeline:
            analysis["recommendations"].append("Timeline non disponible - analyse limitée")
            return analysis
        
        # Analyse des morts suspectes
        deaths = [e for e in timeline if e.event_type == "death"]
        
        # Morts en early game
        early_deaths = [d for d in deaths if d.timestamp < 900]  # < 15 min
        if len(early_deaths) >= 3:
            analysis["critical"].append(f"Trop de morts en early game: {len(early_deaths)}")
            analysis["recommendations"].append("Phase de lane trop aggressive - joue plus safe en early")
            analysis["score"] -= 20
        
        # Morts répétées au même endroit
        death_positions = [d.position for d in deaths if d.position]
        if len(death_positions) > 2:
            # Vérifier les positions similaires (simplified)
            analysis["weaknesses"].append("Plusieurs morts dans les mêmes zones")
            analysis["recommendations"].append("Ces zones sont dangereuses - utilise plus de vision avant d'y aller")
        
        # Temps passé mort
        game_duration_min = metrics.game_duration / 60
        death_time_ratio = (metrics.time_spent_dead / metrics.game_duration) * 100
        
        if death_time_ratio > 15:
            analysis["critical"].append(f"Trop de temps passé mort: {death_time_ratio:.1f}%")
            analysis["recommendations"].append("Chaque mort = opportunités perdues - focus réduction deaths")
            analysis["score"] -= 15
        
        return analysis
    
    def analyze_timeline(self, timeline: List[TimelineEvent], 
                        metrics: GameMetrics) -> List[Dict]:
        """Analyse détaillée de la timeline"""
        insights = []
        
        # Phases de jeu
        early = [e for e in timeline if e.timestamp < 900]  # 0-15 min
        mid = [e for e in timeline if 900 <= e.timestamp < 1800]  # 15-30 min
        late = [e for e in timeline if e.timestamp >= 1800]  # 30+ min
        
        # Analyse early game
        early_deaths = [e for e in early if e.event_type == "death"]
        if len(early_deaths) >= 2:
            insights.append({
                "phase": "Early Game (0-15 min)",
                "issue": f"{len(early_deaths)} morts en early",
                "severity": "critical",
                "advice": "Phase de lane trop aggressive - respect l'ennemi et sa jungle"
            })
        
        # Analyse mid game
        mid_deaths = [e for e in mid if e.event_type == "death"]
        if len(mid_deaths) >= 3:
            insights.append({
                "phase": "Mid Game (15-30 min)",
                "issue": f"{len(mid_deaths)} morts en mid game",
                "severity": "warning",
                "advice": "Évite de farm solo sans vision - groupe avec ton équipe"
            })
        
        # Analyse late game
        late_deaths = [e for e in late if e.event_type == "death"]
        if len(late_deaths) >= 2:
            insights.append({
                "phase": "Late Game (30+ min)",
                "issue": f"{len(late_deaths)} morts en late game",
                "severity": "critical",
                "advice": "Les morts en late coûtent la game - joue ultra safe"
            })
        
        return insights
    
    def generate_advice_priority(self, analysis: Dict) -> List[str]:
        """Génère une liste priorisée de conseils"""
        priorities = []
        
        # Critiques en premier
        if analysis["critical_issues"]:
            priorities.append("🚨 PRIORITÉS CRITIQUES:")
            for issue in analysis["critical_issues"][:3]:
                priorities.append(f"  • {issue}")
        
        # Top 3 recommendations
        if analysis["recommendations"]:
            priorities.append("\n💡 TOP RECOMMANDATIONS:")
            for rec in analysis["recommendations"][:5]:
                priorities.append(f"  • {rec}")
        
        # Points forts à maintenir
        if analysis["strengths"]:
            priorities.append("\n✅ POINTS FORTS À MAINTENIR:")
            for strength in analysis["strengths"][:3]:
                priorities.append(f"  • {strength}")
        
        return priorities
    
    def get_rank_estimate(self, overall_score: float) -> str:
        """Estime le rank basé sur le score global"""
        if overall_score >= 90:
            return "Diamond+"
        elif overall_score >= 80:
            return "Platinum"
        elif overall_score >= 70:
            return "Gold"
        elif overall_score >= 60:
            return "Silver"
        elif overall_score >= 50:
            return "Bronze"
        else:
            return "Iron"


def create_sample_game() -> Tuple[GameMetrics, List[TimelineEvent]]:
    """Crée un exemple de partie pour démonstration"""
    metrics = GameMetrics(
        game_duration=1800,  # 30 minutes
        champion="Ahri",
        role="Mid",
        total_cs=180,
        cs_per_min=6.0,
        jungle_cs=20,
        kills=5,
        deaths=7,
        assists=8,
        kda=1.86,
        damage_dealt=24000,
        damage_taken=18000,
        damage_per_min=800,
        vision_score=25,
        wards_placed=15,
        wards_destroyed=3,
        control_wards_bought=3,
        turret_plates=2,
        turrets_destroyed=1,
        dragons_secured=1,
        barons_secured=0,
        objective_participation=50.0,  # 50% des objectifs
        gold_earned=12000,
        gold_per_min=400,
        time_cc_others=45.0,
        time_spent_dead=180,
        team_average_kda=2.4,  # KDA moyen des alliés
        nemesis_champion="Zed"  # Champion problématique
    )
    
    timeline = [
        TimelineEvent(300, "death", (5000, 7000), "Mort en 1v1 en lane", "warning"),
        TimelineEvent(600, "death", (5000, 7000), "Mort encore en lane", "critical"),
        TimelineEvent(900, "kill", (6000, 6000), "Kill sur jungler ennemi", "info"),
        TimelineEvent(1200, "death", (4000, 4000), "Mort en gank", "warning"),
        TimelineEvent(1500, "objective", None, "Dragon pris", "info"),
        TimelineEvent(1650, "death", (5000, 5000), "Mort en teamfight", "warning"),
    ]
    
    return metrics, timeline

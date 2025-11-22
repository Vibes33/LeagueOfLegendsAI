"""
Exemples d'utilisation du système d'analyse gameplay
"""

from gameplay_analyzer import GameplayAnalyzer, create_sample_game
from colorama import Fore, Style, init

init(autoreset=True)


def example_full_analysis():
    """Exemple d'analyse complète d'une partie"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}ANALYSE DE GAMEPLAY - EXEMPLE COMPLET")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    # Créer une partie exemple
    metrics, timeline = create_sample_game()
    
    print(f"{Fore.YELLOW}Partie analysée:")
    print(f"  Champion: {Fore.WHITE}{metrics.champion}")
    print(f"  Rôle: {Fore.WHITE}{metrics.role}")
    print(f"  Durée: {Fore.WHITE}{metrics.game_duration // 60} minutes")
    print(f"  KDA: {Fore.WHITE}{metrics.kills}/{metrics.deaths}/{metrics.assists} ({metrics.kda:.2f})")
    print(f"  CS: {Fore.WHITE}{metrics.total_cs} ({metrics.cs_per_min:.1f}/min)\n")
    
    # Analyse
    analyzer = GameplayAnalyzer()
    analysis = analyzer.analyze_game(metrics, timeline)
    
    # Score global
    score = analysis["overall_score"]
    rank_estimate = analyzer.get_rank_estimate(score)
    
    score_color = Fore.GREEN if score >= 75 else Fore.YELLOW if score >= 50 else Fore.RED
    print(f"{Fore.CYAN}{Style.BRIGHT}SCORE GLOBAL: {score_color}{score:.1f}/100")
    print(f"{Fore.CYAN}Niveau estimé: {Fore.WHITE}{rank_estimate}\n")
    
    # Scores par catégorie
    print(f"{Fore.CYAN}{Style.BRIGHT}SCORES PAR CATÉGORIE:\n")
    for category, cat_score in analysis["category_scores"].items():
        color = Fore.GREEN if cat_score >= 75 else Fore.YELLOW if cat_score >= 50 else Fore.RED
        bar_length = int(cat_score / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"{Fore.WHITE}{category:<30} {color}{bar} {cat_score:.0f}/100")
    
    print()
    
    # Problèmes critiques
    if analysis["critical_issues"]:
        print(f"{Fore.RED}{Style.BRIGHT}🚨 PROBLÈMES CRITIQUES:\n")
        for issue in analysis["critical_issues"]:
            print(f"{Fore.RED}  ✗ {issue}")
        print()
    
    # Points à améliorer
    if analysis["weaknesses"]:
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  POINTS À AMÉLIORER:\n")
        for weakness in analysis["weaknesses"][:5]:
            print(f"{Fore.YELLOW}  • {weakness}")
        print()
    
    # Points forts
    if analysis["strengths"]:
        print(f"{Fore.GREEN}{Style.BRIGHT}✅ POINTS FORTS:\n")
        for strength in analysis["strengths"][:5]:
            print(f"{Fore.GREEN}  ✓ {strength}")
        print()
    
    # Recommandations
    if analysis["recommendations"]:
        print(f"{Fore.CYAN}{Style.BRIGHT}💡 RECOMMANDATIONS:\n")
        for i, rec in enumerate(analysis["recommendations"][:7], 1):
            print(f"{Fore.CYAN}  {i}. {Fore.WHITE}{rec}")
        print()
    
    # Analyse de timeline
    if analysis["timeline_analysis"]:
        print(f"{Fore.MAGENTA}{Style.BRIGHT}📊 ANALYSE PAR PHASE:\n")
        for insight in analysis["timeline_analysis"]:
            severity_color = Fore.RED if insight["severity"] == "critical" else Fore.YELLOW
            print(f"{severity_color}  [{insight['phase']}]")
            print(f"{Fore.WHITE}    Issue: {insight['issue']}")
            print(f"{Fore.LIGHTBLACK_EX}    Conseil: {insight['advice']}\n")
    
    print(f"{Fore.CYAN}{'='*70}\n")


def example_comparison():
    """Exemple de comparaison entre deux parties"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}COMPARAISON DE DEUX PARTIES")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    analyzer = GameplayAnalyzer()
    
    # Partie 1 (mauvaise)
    metrics1, timeline1 = create_sample_game()
    analysis1 = analyzer.analyze_game(metrics1, timeline1)
    
    # Partie 2 (bonne) - simule une amélioration
    from gameplay_analyzer import GameMetrics
    metrics2 = GameMetrics(
        game_duration=1800,
        champion="Ahri",
        role="Mid",
        total_cs=240,
        cs_per_min=8.0,
        jungle_cs=30,
        kills=10,
        deaths=3,
        assists=12,
        kda=7.33,
        damage_dealt=32000,
        damage_taken=15000,
        damage_per_min=1067,
        vision_score=35,
        wards_placed=20,
        wards_destroyed=8,
        control_wards_bought=6,
        turret_plates=4,
        turrets_destroyed=3,
        dragons_secured=2,
        barons_secured=1,
        gold_earned=15000,
        gold_per_min=500,
        time_cc_others=60.0,
        time_spent_dead=60
    )
    analysis2 = analyzer.analyze_game(metrics2)
    
    print(f"{Fore.YELLOW}PARTIE 1 (Avant):  {Fore.RED}Score: {analysis1['overall_score']:.1f}/100")
    print(f"{Fore.YELLOW}PARTIE 2 (Après): {Fore.GREEN}Score: {analysis2['overall_score']:.1f}/100")
    print(f"{Fore.CYAN}Progression: {Fore.GREEN}+{analysis2['overall_score'] - analysis1['overall_score']:.1f} points 📈\n")
    
    print(f"{Fore.CYAN}{Style.BRIGHT}COMPARAISON PAR CATÉGORIE:\n")
    
    for category in analysis1["category_scores"].keys():
        score1 = analysis1["category_scores"][category]
        score2 = analysis2["category_scores"][category]
        diff = score2 - score1
        
        diff_color = Fore.GREEN if diff > 0 else Fore.RED if diff < 0 else Fore.WHITE
        diff_symbol = "↑" if diff > 0 else "↓" if diff < 0 else "="
        
        print(f"{Fore.WHITE}{category:<30}")
        print(f"  Avant:  {Fore.RED}{score1:>5.1f}/100")
        print(f"  Après:  {Fore.GREEN}{score2:>5.1f}/100")
        print(f"  {diff_color}Diff:   {diff_symbol} {abs(diff):>5.1f}\n")
    
    print(f"{Fore.CYAN}{'='*70}\n")


def example_quick_tips():
    """Conseils rapides basés sur l'analyse"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}CONSEILS PRIORITAIRES")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    metrics, timeline = create_sample_game()
    analyzer = GameplayAnalyzer()
    analysis = analyzer.analyze_game(metrics, timeline)
    
    priorities = analyzer.generate_advice_priority(analysis)
    
    for line in priorities:
        if "PRIORITÉS" in line or "RECOMMANDATIONS" in line or "POINTS FORTS" in line:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}{line}")
        else:
            print(line)
    
    print(f"\n{Fore.CYAN}{'='*70}\n")


def example_role_comparison():
    """Montre les benchmarks par rôle"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}BENCHMARKS PAR RÔLE")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    analyzer = GameplayAnalyzer()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'Rôle':<12} {'CS/min':<10} {'Vision/min':<12} {'Damage/min':<12} {'KDA Target'}")
    print(f"{Fore.BLUE}{'-'*70}")
    
    for role, benchmarks in analyzer.benchmarks.items():
        print(f"{Fore.GREEN}{role:<12} "
              f"{Fore.WHITE}{benchmarks['cs_per_min']:<10.1f} "
              f"{Fore.CYAN}{benchmarks['vision_score_per_min']:<12.1f} "
              f"{Fore.MAGENTA}{benchmarks['damage_per_min']:<12.0f} "
              f"{Fore.YELLOW}{benchmarks['kda_target']:.1f}")
    
    print(f"\n{Fore.LIGHTBLACK_EX}Ces benchmarks sont des moyennes pour Iron-Gold rank")
    print(f"{Fore.CYAN}{'='*70}\n")


def main():
    """Execute tous les exemples"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}     SYSTÈME D'ANALYSE GAMEPLAY - DÉMONSTRATION")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    examples = [
        ("Analyse Complète", example_full_analysis),
        ("Comparaison de Parties", example_comparison),
        ("Conseils Prioritaires", example_quick_tips),
        ("Benchmarks par Rôle", example_role_comparison)
    ]
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"{Fore.YELLOW}[{i}] {name}")
    
    print(f"\n{Fore.CYAN}Appuyez sur Entrée pour voir chaque exemple...\n")
    
    for name, func in examples:
        input(f"{Fore.CYAN}▶ {name}... ")
        func()


if __name__ == "__main__":
    main()

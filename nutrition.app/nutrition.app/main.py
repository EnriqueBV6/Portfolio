"""
Main script for Nutrition & Training Planner.

This script demonstrates the complete functionality of the nutrition planner
with example user profiles and detailed analysis output.
"""

from models.user_profile import UserProfile
from services.metabolic_service import calculate_metabolic_profile
from services.nutrition_service import calculate_nutritional_profile
from services.recommendation_engine import generate_complete_recommendation


def print_separator(title: str) -> None:
    """Print a formatted separator with title."""
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "="))
    print("=" * 60)


def print_user_profile(user_profile: UserProfile) -> None:
    """Print user profile information."""
    print(f"PERFIL DE USUARIO")
    print(f"   Peso: {user_profile.weight} kg")
    print(f"   Altura: {user_profile.height} cm")
    print(f"   Edad: {user_profile.age} años")
    print(f"   Sexo: {user_profile.sex}")
    print(f"   Nivel de actividad: {user_profile.activity_level}")
    print(f"   Objetivo: {user_profile.goal}")


def print_metabolic_results(metabolic_result) -> None:
    """Print metabolic calculation results."""
    print(f"\nANALISIS METABOLICO")
    print(f"   Tasa Metabolica Basal (BMR): {metabolic_result.bmr:.0f} kcal/dia")
    print(f"   Gasto Energetico Total (TDEE): {metabolic_result.tdee:.0f} kcal/dia")
    print(f"   Factor de actividad: {metabolic_result.activity_factor:.2f}")


def print_nutritional_results(nutritional_result) -> None:
    """Print nutritional calculation results."""
    print(f"\nANALISIS NUTRICIONAL")
    print(f"   Balance energetico actual: {nutritional_result.energy_balance:+.0f} kcal")
    print(f"   Estado metabolico: {nutritional_result.status}")
    print(f"   Calorias objetivo: {nutritional_result.target_calories:.0f} kcal/dia")
    
    print(f"\n   Distribución de macronutrientes:")
    print(f"   • Proteína: {nutritional_result.macro_split['protein']:.1f}g "
          f"({nutritional_result.macro_percentages['protein']:.1f}%)")
    print(f"   • Grasas: {nutritional_result.macro_split['fat']:.1f}g "
          f"({nutritional_result.macro_percentages['fat']:.1f}%)")
    print(f"   • Carbohidratos: {nutritional_result.macro_split['carbs']:.1f}g "
          f"({nutritional_result.macro_percentages['carbs']:.1f}%)")


def print_recommendations(recommendation_result) -> None:
    """Print recommendation results."""
    print(f"\nRECOMENDACIONES PERSONALIZADAS")
    print(f"   Nivel de confianza: {recommendation_result.confidence_level:.1%}")
    print(f"\n   {recommendation_result.recommendation}")
    
    print(f"\nPASOS ACCIONABLES:")
    for i, step in enumerate(recommendation_result.actionable_steps, 1):
        print(f"   {i}. {step}")


def analyze_user(user_profile: UserProfile, current_calories: float = 0.0, training_calories: float = 0.0) -> None:
    """
    Perform complete analysis for a user.
    
    Args:
        user_profile: User's profile data
        current_calories: Current daily calorie intake
        training_calories: Calories burned through training
    """
    # Calculate metabolic profile
    metabolic_result = calculate_metabolic_profile(user_profile)
    
    # Calculate nutritional profile
    nutritional_result = calculate_nutritional_profile(
        user_profile=user_profile,
        metabolic_result=metabolic_result,
        current_calories=current_calories,
        training_calories=training_calories
    )
    
    # Generate recommendations
    recommendation_result = generate_complete_recommendation(
        user_profile=user_profile,
        metabolic_result=metabolic_result,
        nutritional_result=nutritional_result
    )
    
    # Print all results
    print_user_profile(user_profile)
    print_metabolic_results(metabolic_result)
    print_nutritional_results(nutritional_result)
    print_recommendations(recommendation_result)


def main() -> None:
    """Main function demonstrating the nutrition planner."""
    print("NUTRITION & TRAINING PLANNER - DEMONSTRATION")
    print("Motor de decision para planificacion nutricional y de entrenamiento")
    
    # Example 1: User wanting to lose weight
    print_separator("CASO 1: PÉRDIDA DE PESO (DÉFICIT)")
    user1 = UserProfile(
        weight=85.0,
        height=175.0,
        age=32,
        sex="male",
        activity_level="moderate",
        goal="deficit"
    )
    analyze_user(user1, current_calories=2200, training_calories=300)
    
    # Example 2: User wanting to gain muscle
    print_separator("CASO 2: GANANCIA MUSCULAR (VOLUMEN)")
    user2 = UserProfile(
        weight=70.0,
        height=180.0,
        age=25,
        sex="male",
        activity_level="high",
        goal="bulk"
    )
    analyze_user(user2, current_calories=2800, training_calories=400)
    
    # Example 3: User wanting to maintain weight
    print_separator("CASO 3: MANTENIMIENTO")
    user3 = UserProfile(
        weight=60.0,
        height=165.0,
        age=28,
        sex="female",
        activity_level="light",
        goal="maintenance"
    )
    analyze_user(user3, current_calories=1900, training_calories=200)
    
    # Example 4: Sedentary user wanting to lose weight
    print_separator("CASO 4: USUARIO SEDENTARIO - PÉRDIDA DE PESO")
    user4 = UserProfile(
        weight=95.0,
        height=170.0,
        age=45,
        sex="male",
        activity_level="sedentary",
        goal="deficit"
    )
    analyze_user(user4, current_calories=2000, training_calories=0)
    
    print_separator("FIN DE LA DEMONSTRATION")
    print("Todos los calculos completados exitosamente")
    print("El sistema esta listo para integracion con FastAPI o Flask")


if __name__ == "__main__":
    main()

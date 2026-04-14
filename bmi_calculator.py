class BMICalculator:
    """Handles BMI calculation and categorization with validation"""
    
    # WHO BMI Categories
    CATEGORIES = {
        'Underweight': {'range': (0, 18.4), 'color': '#FF6B6B'},
        'Normal': {'range': (18.5, 24.9), 'color': '#4ECDC4'},
        'Overweight': {'range': (25.0, 29.9), 'color': '#FFE66D'},
        'Obese': {'range': (30.0, float('inf')), 'color': '#FF8B94'}
    }
    
    @staticmethod
    def calculate_bmi(weight_kg, height_m):
        """Calculate BMI using formula: weight / (height^2)"""
        if height_m <= 0:
            raise ValueError("Height must be greater than 0")
        if weight_kg <= 0:
            raise ValueError("Weight must be greater than 0")
        return weight_kg / (height_m ** 2)
    
    @staticmethod
    def categorize_bmi(bmi):
        """Categorize BMI into health ranges"""
        for category, data in BMICalculator.CATEGORIES.items():
            if data['range'][0] <= bmi < data['range'][1]:
                return category, data['color']
        return "Unknown", "#808080"
    
    @staticmethod
    def validate_inputs(weight_str, height_str):
        """Validate user inputs"""
        try:
            weight = float(weight_str)
            height = float(height_str)
            
            if weight < 1 or weight > 1000:
                raise ValueError("Weight must be between 1-1000 kg")
            if height < 0.1 or height > 3.0:
                raise ValueError("Height must be between 0.1-3.0 meters")
                
            return weight, height
        except ValueError as e:
            raise ValueError(f"Invalid input: {str(e)}")
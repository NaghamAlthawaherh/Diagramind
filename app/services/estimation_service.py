import math
import random

class EffortEstimator:
    """
    Effort Estimator service that implements Function Point Analysis and
    Use Case Points methods to estimate project effort, duration, and cost.
    """
    
    def __init__(self):
        # Constants for Function Point Analysis
        self.fp_complexity_weights = {
            'Simple': {
                'input': 3,
                'output': 4, 
                'inquiry': 3,
                'file': 7,
                'interface': 5
            },
            'Average': {
                'input': 4,
                'output': 5,
                'inquiry': 4,
                'file': 10,
                'interface': 7
            },
            'Complex': {
                'input': 6,
                'output': 7,
                'inquiry': 6,
                'file': 15,
                'interface': 10
            }
        }
        
        # Constants for Use Case Points
        self.ucp_actor_weights = {
            'Simple': 1,   # API, external system
            'Average': 2,  # Another system through a protocol
            'Complex': 3   # Human with GUI interaction
        }
        
        self.ucp_use_case_weights = {
            'Simple': 5,    # 1-3 transactions
            'Average': 10,  # 4-7 transactions
            'Complex': 15   # >7 transactions
        }
        
        # Technical and environmental factors
        self.technical_factors = {
            'distributed_system': 2.0,
            'performance_objectives': 1.0,
            'end_user_efficiency': 1.0,
            'complex_processing': 1.0,
            'reusable_code': 1.0,
            'easy_to_install': 0.5,
            'easy_to_use': 0.5,
            'portable': 2.0,
            'easy_to_change': 1.0,
            'concurrent_users': 1.0,
            'security_features': 1.0,
            'third_party_access': 1.0,
            'user_training': 1.0
        }
        
        self.environmental_factors = {
            'familiar_with_process': 1.5,
            'application_experience': 0.5,
            'object_oriented_experience': 1.0,
            'lead_analyst_capability': 0.5,
            'motivation': 1.0,
            'stable_requirements': 2.0,
            'part_time_workers': -1.0,
            'difficult_programming_language': -1.0
        }
        
        # Cost factors
        self.avg_salary_per_month = 7500  # Average developer salary in USD
        self.overhead_factor = 1.5  # Overhead multiplier for facilities, managers, etc.
        self.contingency_rate = 0.15  # Contingency for unforeseen expenses
    
    def calculate_function_points(self, use_cases, actors):
        """
        Calculate unadjusted function points based on actors and use cases
        
        Args:
            use_cases: List of use cases with complexity data
            actors: List of actors
            
        Returns:
            Total function points
        """
        total_fp = 0
        
        # Map each use case to FP component types
        for uc in use_cases:
            complexity = uc.get('complexity', 'Average')
            uc_name = uc.get('name', '').lower()
            
            # Determine which FP components apply to this use case
            if 'report' in uc_name or 'view' in uc_name or 'display' in uc_name:
                # Output type
                total_fp += self.fp_complexity_weights[complexity]['output']
                
            elif 'search' in uc_name or 'find' in uc_name or 'query' in uc_name:
                # Inquiry type
                total_fp += self.fp_complexity_weights[complexity]['inquiry']
                
            elif 'add' in uc_name or 'create' in uc_name or 'register' in uc_name or 'input' in uc_name:
                # Input type
                total_fp += self.fp_complexity_weights[complexity]['input']
                
            elif 'manage' in uc_name or 'maintain' in uc_name or 'store' in uc_name:
                # File type (internal data)
                total_fp += self.fp_complexity_weights[complexity]['file']
                
            elif 'integrate' in uc_name or 'connect' in uc_name or 'interface' in uc_name:
                # Interface type (external data)
                total_fp += self.fp_complexity_weights[complexity]['interface']
                
            else:
                # Default to a mix of input and output
                total_fp += self.fp_complexity_weights[complexity]['input']
                total_fp += self.fp_complexity_weights[complexity]['output']
        
        # Add points for each external actor (interfaces)
        for actor in actors:
            actor_type = actor.get('type', 'Primary')
            if 'System' in actor.get('name', '') or actor_type == 'Secondary':
                # External system interface
                total_fp += self.fp_complexity_weights['Average']['interface']
        
        return total_fp
    
    def calculate_use_case_points(self, use_cases, actors):
        """
        Calculate unadjusted use case points
        
        Args:
            use_cases: List of use cases with complexity data
            actors: List of actors
            
        Returns:
            Total use case points
        """
        # Calculate Unadjusted Actor Weight (UAW)
        uaw = 0
        for actor in actors:
            actor_name = actor.get('name', '').lower()
            actor_type = actor.get('type', 'Primary')
            
            if 'system' in actor_name or actor_type == 'Secondary':
                # External system
                weight = self.ucp_actor_weights['Simple']
            else:
                # Human user with GUI
                weight = self.ucp_actor_weights['Complex']
            
            uaw += weight
        
        # Calculate Unadjusted Use Case Weight (UUCW)
        uucw = 0
        for uc in use_cases:
            complexity = uc.get('complexity', 'Average')
            uucw += self.ucp_use_case_weights[complexity]
        
        # Unadjusted Use Case Points
        uucp = uaw + uucw
        
        # For simplicity, we'll use estimated Technical Complexity Factor (TCF)
        # and Environmental Factor (EF) values
        tcf = 0.85  # Typical value between 0.6 and 1.3
        ef = 0.85   # Typical value between 0.5 and 1.5
        
        # Adjusted Use Case Points
        ucp = uucp * tcf * ef
        
        return ucp
    
    def estimate_effort(self, use_cases, actors, requirements):
        """
        Estimate project effort, duration, cost, and generate recommendations
        
        Args:
            use_cases: List of use cases
            actors: List of actors
            requirements: List of requirements
            
        Returns:
            Dictionary with estimation details
        """
        # Calculate Function Points
        fp = self.calculate_function_points(use_cases, actors)
        
        # Calculate Use Case Points
        ucp = self.calculate_use_case_points(use_cases, actors)
        
        # Calculate complexity factors based on requirements distribution
        req_categories = {}
        for req in requirements:
            category = req.get('category', 'Functional')
            req_categories[category] = req_categories.get(category, 0) + 1
        
        # More non-functional requirements usually indicate higher complexity
        total_reqs = len(requirements) if requirements else 1
        nfr_ratio = 1 - (req_categories.get('Functional', 0) / total_reqs)
        complexity_factor = 1.0 + (nfr_ratio * 0.3)  # 1.0 to 1.3 based on NFR ratio
        
        # Effort estimation: hours per function point or use case point
        # Industry standard: 8-16 hours per function point
        hours_per_fp = 12 * complexity_factor
        hours_per_ucp = 20 * complexity_factor
        
        # Calculate effort in hours
        fp_effort_hours = fp * hours_per_fp
        ucp_effort_hours = ucp * hours_per_ucp
        
        # Average the two methods
        effort_hours = (fp_effort_hours + ucp_effort_hours) / 2
        
        # Convert to person-months (assuming 160 hours per month)
        person_months = effort_hours / 160
        
        # Determine appropriate team size
        team_size = self._determine_team_size(person_months)
        
        # Calculate project duration in months
        duration_months = person_months / team_size
        
        # Round to the nearest half month
        duration_months = round(duration_months * 2) / 2
        
        # Format duration as a string
        if duration_months < 1:
            duration_str = f"{int(duration_months * 30)} days"
        else:
            duration_str = f"{duration_months:.1f} months"
        
        # Determine team size range
        team_min = max(1, int(team_size * 0.8))
        team_max = int(team_size * 1.2) + 1
        team_size_str = f"{team_min}-{team_max} developers"
        
        # Calculate cost
        monthly_labor_cost = team_size * self.avg_salary_per_month
        total_labor_cost = monthly_labor_cost * duration_months
        
        # Add overhead
        total_cost_with_overhead = total_labor_cost * self.overhead_factor
        
        # Add contingency
        total_cost_with_contingency = total_cost_with_overhead * (1 + self.contingency_rate)
        
        # Calculate min and max labor costs (±10%)
        labor_cost_min = int(total_labor_cost * 0.9)
        labor_cost_max = int(total_labor_cost * 1.1)
        
        # Calculate min and max additional costs (hardware, licenses, etc.)
        additional_cost_min = int(total_labor_cost * 0.15)
        additional_cost_max = int(total_labor_cost * 0.25)
        
        # Determine risk level
        risk_level = self._determine_risk_level(use_cases, requirements, complexity_factor, actors)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(use_cases, actors, requirements, risk_level)
        
        # Effort distribution (typical percentages)
        effort_distribution = {
            'analysis': 15,
            'design': 20,
            'development': 40,
            'testing': 15,
            'deployment': 10
        }
        
        # Return all estimation details
        return {
            'function_points': int(fp),
            'complexity_factor': int(complexity_factor * 100),  # Store as integer percentage
            'use_case_points': int(ucp),
            'technical_complexity': int(0.85 * 100),  # Default TCF as integer percentage
            'estimated_duration': duration_str,
            'estimated_team_size': team_size_str,
            'person_months': int(person_months),
            'labor_cost_min': labor_cost_min,
            'labor_cost_max': labor_cost_max,
            'additional_cost_min': additional_cost_min,
            'additional_cost_max': additional_cost_max,
            'risk_level': risk_level,
            'effort_distribution': effort_distribution,
            'recommendations': recommendations
        }
    
    def _determine_team_size(self, person_months):
        """Determine recommended team size based on project size"""
        if person_months <= 3:
            return 1.5  # 1-2 developers
        elif person_months <= 6:
            return 2.5  # 2-3 developers
        elif person_months <= 12:
            return 4    # 3-5 developers
        elif person_months <= 24:
            return 6    # 5-7 developers
        else:
            return 8    # 7+ developers
    
    def _determine_risk_level(self, use_cases, requirements, complexity_factor, actors=[]):
        """Determine project risk level"""
        # Count high priority requirements
        high_priority_count = sum(1 for req in requirements if req.get('priority') in ['High', 'Critical'])
        
        # Count complex use cases
        complex_use_cases = sum(1 for uc in use_cases if uc.get('complexity') == 'Complex')
        
        # External system actors
        external_systems = sum(1 for actor in actors if 'System' in actor.get('name', '') or actor.get('type') == 'Secondary')
        
        # Calculate risk score
        risk_score = 0
        risk_score += high_priority_count * 0.5
        risk_score += complex_use_cases * 1.0
        risk_score += external_systems * 0.5
        risk_score += (complexity_factor - 1.0) * 10  # 0-3 points from complexity factor
        
        # Determine risk level
        if risk_score < 3:
            return 'Low'
        elif risk_score < 6:
            return 'Medium'
        else:
            return 'High'
    
    def _generate_recommendations(self, use_cases, actors, requirements, risk_level):
        """Generate project recommendations based on analysis"""
        recommendations = []
        
        # Find complex use cases
        complex_use_cases = [uc for uc in use_cases if uc.get('complexity') == 'Complex']
        
        # Find external systems
        external_systems = [actor for actor in actors if 'System' in actor.get('name', '') or actor.get('type') == 'Secondary']
        
        # Risk-based recommendations
        if risk_level == 'High':
            recommendations.append('Consider phased implementation to manage high risk elements first.')
            recommendations.append('Implement more frequent review points and milestones to detect issues early.')
            
        if complex_use_cases:
            complex_names = [uc['name'] for uc in complex_use_cases[:2]]  # Get names of up to 2 complex use cases
            recommendations.append(f"Consider splitting the complex use cases (e.g., {', '.join(complex_names)}) into smaller, more manageable components.")
        
        if external_systems:
            recommendations.append('Allocate additional resources to integration with external systems, as these interfaces tend to introduce unexpected complexities.')
        
        # General recommendations
        methodology_rec = 'Implement an incremental development approach with 2-week sprint cycles'
        if risk_level == 'High':
            methodology_rec += ' and weekly demonstrations to stakeholders'
        methodology_rec += ' to better manage the ' + risk_level.lower() + ' complexity level.'
        recommendations.append(methodology_rec)
        
        # Buffer recommendation based on risk
        buffer_percentage = '15%' if risk_level == 'Medium' else '25%' if risk_level == 'High' else '10%'
        recommendations.append(f'Include a {buffer_percentage} buffer in the timeline to account for potential requirement changes and unforeseen technical challenges.')
        
        # Add some variety to recommendations
        potential_recs = [
            'Establish clear acceptance criteria for each use case before beginning development.',
            'Document technical interfaces early, especially for integration with external systems.',
            'Implement continuous integration practices to detect integration issues early.',
            'Allocate sufficient time for non-functional requirements like security and performance testing.',
            'Consider conducting a mid-project architecture review to validate design decisions.',
            'Implement automated testing to ensure stable functionality as the system grows.'
        ]
        
        # Add 2-3 random additional recommendations
        random_recs = random.sample(potential_recs, min(3, len(potential_recs)))
        recommendations.extend(random_recs)
        
        # Limit to 5 recommendations
        return recommendations[:5]

# Singleton instance
effort_estimator = EffortEstimator()


# import time
# import random
# import json

# def generate_estimation(requirements, elements):
#     """
#     Generate project effort estimations based on requirements and diagram elements
    
#     Args:
#         requirements: Extracted requirements
#         elements: Diagram elements
        
#     Returns:
#         Estimation results
#     """
#     # Simulate processing delay
#     simulate_processing_delay(3000)
    
#     # In a real implementation, this would use estimation methods like Function Point Analysis
#     # or Use Case Points to estimate the effort
    
#     # Count use cases and actors for basic estimation
#     num_actors = sum(1 for e in elements if e.get("type") == "actor")
#     num_use_cases = sum(1 for e in elements if e.get("type") == "useCase")
#     num_requirements = len(requirements)
    
#     # Base calculation factors
#     # These would normally be derived from historical project data
#     hours_per_use_case = random.uniform(15, 25)  # Average hours per use case
#     hours_per_requirement = random.uniform(8, 16)  # Average hours per requirement
    
#     # Function Point Analysis - simplified
#     # Calculate function points based on complexity of use cases and number of requirements
#     function_points = num_use_cases * random.uniform(7, 12) + num_requirements * random.uniform(3, 5)
    
#     # Use Case Points calculation - simplified
#     unadjusted_actor_weight = num_actors * random.uniform(1, 3)
#     unadjusted_use_case_weight = num_use_cases * random.uniform(5, 10)
#     use_case_points = unadjusted_actor_weight + unadjusted_use_case_weight
    
#     # Environmental factors (randomly generated for demo)
#     technical_complexity_factor = random.uniform(0.8, 1.2)
#     environmental_factor = random.uniform(0.8, 1.2)
    
#     # Adjust use case points
#     use_case_points *= technical_complexity_factor * environmental_factor
    
#     # Calculate estimated hours
#     estimated_hours = int(function_points * 4 + use_case_points * 20)
    
#     # Generate estimated weeks based on team sizes
#     estimated_weeks = {
#         "small": int(estimated_hours / (3 * 40)) + 1,  # 3 people team
#         "medium": int(estimated_hours / (5 * 40)) + 1,  # 5 people team
#         "large": int(estimated_hours / (8 * 40)) + 1   # 8 people team
#     }
    
#     # Generate recommended team size based on project complexity
#     project_complexity = "medium"
#     if num_use_cases <= 3 and num_requirements <= 5:
#         project_complexity = "small"
#     elif num_use_cases >= 6 or num_requirements >= 12:
#         project_complexity = "large"
        
#     recommended_team_size = {
#         "size": project_complexity,
#         "developers": 3 if project_complexity == "small" else (5 if project_complexity == "medium" else 8),
#         "qa": 1 if project_complexity == "small" else (2 if project_complexity == "medium" else 3),
#         "other": 1 if project_complexity == "small" else (2 if project_complexity == "medium" else 3)
#     }
    
#     # Calculate estimated budget based on average rates
#     hourly_rates = {
#         "developer": random.uniform(80, 120),
#         "qa": random.uniform(60, 90),
#         "pm": random.uniform(100, 150)
#     }
    
#     # Distribution of effort by role
#     effort_distribution = {
#         "development": 0.6,
#         "testing": 0.25,
#         "management": 0.15
#     }
    
#     # Calculate budget by role
#     developer_hours = estimated_hours * effort_distribution["development"]
#     qa_hours = estimated_hours * effort_distribution["testing"]
#     pm_hours = estimated_hours * effort_distribution["management"]
    
#     estimated_budget = {
#         "developer": int(developer_hours * hourly_rates["developer"]),
#         "qa": int(qa_hours * hourly_rates["qa"]),
#         "pm": int(pm_hours * hourly_rates["pm"]),
#         "total": int(developer_hours * hourly_rates["developer"] + 
#                      qa_hours * hourly_rates["qa"] + 
#                      pm_hours * hourly_rates["pm"])
#     }
    
#     # Return the estimation results
#     return {
#         "functionPoints": round(function_points, 2),
#         "useCasePoints": round(use_case_points, 2),
#         "estimatedHours": estimated_hours,
#         "estimatedWeeks": estimated_weeks,
#         "recommendedTeamSize": recommended_team_size,
#         "estimatedBudget": estimated_budget,
#         "effortDistribution": effort_distribution
#     }

# def simulate_processing_delay(ms):
#     """Helper function to simulate processing delay"""
#     time.sleep(ms / 1000)
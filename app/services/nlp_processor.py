import re
import random
from collections import defaultdict

class NLPService:
    """
    Natural Language Processing (NLP) service for analyzing use case text
    and generating functional requirements based on the diagram's components.
    """
    
    def __init__(self):
        # Priority levels and their weights for weighted random selection
        self.priority_levels = {
            'Low': 0.15,
            'Medium': 0.45,
            'High': 0.30,
            'Critical': 0.10
        }
        
        # Complexity levels
        self.complexity_levels = ['Simple', 'Average', 'Complex']
        
        # Requirement categories
        self.requirement_categories = [
            'Functional', 
            'Security',
            'Performance',
            'Usability',
            'Compatibility'
        ]
        
        # Template patterns for requirements
        self.requirement_templates = {
            'user_action': [
                '{actor} shall be able to {action} {object}',
                '{actor} must have the ability to {action} {object}',
                'The system shall allow {actor} to {action} {object}',
                '{actor} shall be permitted to {action} {object} through the system'
            ],
            'system_action': [
                'The system shall {action} {object} for {actor}',
                'The system must {action} {object} when requested by {actor}',
                'The system shall provide functionality to {action} {object} for {actor}',
                'The system is required to {action} {object} on behalf of {actor}'
            ],
            'data_requirement': [
                'The system shall store {object} data including {data_fields}',
                '{object} information including {data_fields} shall be maintained by the system',
                'The system must persist {object} details containing {data_fields}',
                'The system shall maintain records of {object} with {data_fields}'
            ],
            'security_requirement': [
                'The system shall authenticate {actor} before allowing access to {object}',
                'Access to {object} shall be restricted to authorized {actor}',
                'The system must ensure that {object} is secured from unauthorized access',
                'The system shall implement {security_mechanism} for protecting {object}'
            ],
            'performance_requirement': [
                'The system shall process {action} requests within {time_frame}',
                'Response time for {action} operations shall not exceed {time_frame}',
                'The system must complete {action} with a maximum latency of {time_frame}',
                'The system performance for {action} shall be within {time_frame}'
            ]
        }
    
    def _extract_key_concepts(self, text):
        """
        Extract key concepts from use case text
        """
        # Split into words and remove common prepositions, articles, etc.
        stop_words = ['a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'of']
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if word not in stop_words]
    
    def _extract_noun_phrases(self, text):
        """
        Extract potential noun phrases from the text
        Simple implementation without NLP library dependencies
        """
        # Pattern for simple noun phrases (adjective + noun)
        patterns = [
            r'\b([A-Z][a-z]+\s+[A-Z]?[a-z]+)',  # Capitalized word pairs
            r'\b([a-z]+\s+[a-z]+(?:\s+[a-z]+)?)'  # Any word pairs or triplets
        ]
        
        results = []
        for pattern in patterns:
            results.extend(re.findall(pattern, text))
            
        return list(set(results))
    
    def _generate_data_type(self, use_case_name):
        """Generate appropriate data type based on use case name"""
        name_lower = use_case_name.lower()
        
        if 'login' in name_lower or 'authenticate' in name_lower:
            return "user credentials"
        elif 'register' in name_lower or 'create account' in name_lower:
            return "user profile data"
        elif 'payment' in name_lower or 'transaction' in name_lower:
            return "payment details"
        elif 'order' in name_lower or 'purchase' in name_lower:
            return "order information"
        elif 'search' in name_lower or 'find' in name_lower:
            return "search criteria"
        elif 'report' in name_lower or 'analytics' in name_lower:
            return "report parameters"
        elif 'schedule' in name_lower or 'appointment' in name_lower:
            return "schedule information"
        elif 'message' in name_lower or 'notification' in name_lower:
            return "message content"
        else:
            return "relevant data"
    
    def _generate_requirement_id(self, category, index):
        """Generate a requirement ID"""
        prefix = category[0:2].upper()  # FR for Functional, SE for Security, etc.
        return f"{prefix}-{index+1:03d}"
    
    def _select_priority(self):
        """Select a priority level with weighted distribution"""
        levels = list(self.priority_levels.keys())
        weights = list(self.priority_levels.values())
        return random.choices(levels, weights=weights, k=1)[0]
    
    def _estimate_complexity(self, use_case_name, actors_count):
        """Estimate use case complexity based on name and number of actors"""
        name_lower = use_case_name.lower()
        
        # Higher complexity for certain keywords
        complex_keywords = ['manage', 'process', 'analyze', 'integrate', 'generate', 'calculate', 'validate']
        simple_keywords = ['view', 'display', 'show', 'login', 'logout', 'register']
        
        for keyword in complex_keywords:
            if keyword in name_lower:
                return 'Complex'
                
        for keyword in simple_keywords:
            if keyword in name_lower:
                return 'Simple'
        
        # Based on number of actors
        if actors_count >= 3:
            return 'Complex'
        elif actors_count == 2:
            return 'Average'
        else:
            return 'Simple'
    
    def generate_requirements(self, use_cases, actors, connections):
        """
        Generate functional requirements based on use cases and actors
        
        Args:
            use_cases: List of use cases with names
            actors: List of actors with names
            connections: Dictionary mapping actor indices to use case indices
            
        Returns:
            List of requirements
        """
        requirements = []
        req_index = 0
        
        # Invert connections to get actors for each use case
        use_case_actors = defaultdict(list)
        for actor_idx, use_case_indices in connections.items():
            for uc_idx in use_case_indices:
                use_case_actors[uc_idx].append(actor_idx)
        
        # For each use case, generate several requirements
        for i, use_case in enumerate(use_cases):
            use_case_name = use_case['name']
            actor_indices = use_case_actors.get(i, [])
            
            # Determine use case complexity
            complexity = self._estimate_complexity(use_case_name, len(actor_indices))
            
            # Number of requirements to generate based on complexity
            num_reqs = 2 if complexity == 'Simple' else 3 if complexity == 'Average' else 4
            
            # Extract key concepts from the use case name
            concepts = self._extract_key_concepts(use_case_name)
            
            # Generate different types of requirements
            for j in range(num_reqs):
                # Decide on requirement category
                category = 'Functional' if j == 0 else random.choice(self.requirement_categories)
                
                # Generate requirement ID
                req_id = self._generate_requirement_id(category, req_index)
                req_index += 1
                
                # Select priority
                priority = self._select_priority()
                
                # Determine which actors are involved
                involved_actor_indices = []
                if actor_indices:
                    # Use all actors for the first requirement, then randomly select for others
                    if j == 0:
                        involved_actor_indices = actor_indices
                    else:
                        # Select at least one actor, up to all actors
                        num_actors = random.randint(1, len(actor_indices))
                        involved_actor_indices = random.sample(actor_indices, num_actors)
                
                # Get actor names
                actor_names = [actors[idx]['name'] for idx in involved_actor_indices if idx < len(actors)]
                if not actor_names:
                    actor_names = ['User']  # Default if no actors are found
                
                # Generate description based on category
                description = ""
                if category == 'Functional':
                    # Select template type based on actor type
                    is_system_actor = any('system' in actor['name'].lower() for actor in actors if actor['id']-1 in involved_actor_indices)
                    template_type = 'system_action' if is_system_actor else 'user_action'
                    
                    # Select a template
                    template = random.choice(self.requirement_templates[template_type])
                    
                    # Extract verb and object from use case name or generate
                    verb_obj_match = re.search(r'(\w+)\s+(.*)', use_case_name)
                    if verb_obj_match:
                        action = verb_obj_match.group(1).lower()
                        obj = verb_obj_match.group(2)
                    else:
                        action = "access" if "login" in concepts else "manage" if "admin" in concepts else "perform"
                        obj = use_case_name
                    
                    # Format the template
                    actor_str = actor_names[0] if len(actor_names) == 1 else "authorized users"
                    description = template.format(actor=actor_str, action=action, object=obj)
                    
                elif category == 'Security':
                    template = random.choice(self.requirement_templates['security_requirement'])
                    actor_str = actor_names[0] if len(actor_names) == 1 else "authorized users"
                    security_mechanisms = ['role-based access control', 'authentication tokens', 'encryption', 'secure sessions']
                    description = template.format(
                        actor=actor_str, 
                        object=use_case_name, 
                        security_mechanism=random.choice(security_mechanisms)
                    )
                    
                elif category == 'Performance':
                    template = random.choice(self.requirement_templates['performance_requirement'])
                    time_frames = ['500ms', '1 second', '3 seconds', '5 seconds']
                    action = concepts[0] if concepts else "processing"
                    description = template.format(action=action, time_frame=random.choice(time_frames))
                    
                elif category == 'Usability':
                    description = f"The {use_case_name} interface shall be intuitive and require no more than 3 steps to complete the task."
                    
                elif category == 'Compatibility':
                    description = f"The {use_case_name} functionality shall work consistently across modern web browsers including Chrome, Firefox, Safari, and Edge."
                
                # Create requirement
                requirement = {
                    'req_id': req_id,
                    'description': description,
                    'priority': priority,
                    'category': category,
                    'use_case_id': use_case['id'],
                    'actors': involved_actor_indices
                }
                
                requirements.append(requirement)
                
        return requirements

# Singleton instance
nlp_service = NLPService()



# import time
# import random

# def analyze_requirements(elements):
#     """
#     Analyze diagram elements to extract structured requirements
    
#     Args:
#         elements: Diagram elements with extracted text
        
#     Returns:
#         Array of structured requirements
#     """
#     # Simulate processing delay
#     simulate_processing_delay(2500)
    
#     # In a real implementation, this would use NLP techniques to extract requirements
#     # from the text content of each element
    
#     requirements = []
    
#     priority_levels = ["high", "medium", "low"]
#     requirement_types = ["functional", "non-functional", "technical"]
    
#     for element in elements:
#         # Only generate requirements for use cases
#         if element.get("type") != "useCase":
#             continue
            
#         use_case_text = element.get("text", "")
#         if not use_case_text:
#             continue
            
#         # Generate 1-2 requirements for each use case
#         num_requirements = random.randint(1, 2)
        
#         for i in range(num_requirements):
#             # Use case text typically has the format "verb noun"
#             # We'll transform this into a requirement statement
            
#             if " " in use_case_text:
#                 verb, noun = use_case_text.split(" ", 1)
#             else:
#                 verb, noun = use_case_text, "functionality"
                
#             # Requirement templates based on use case text
#             templates = [
#                 f"The system shall allow users to {verb.lower()} {noun}",
#                 f"Users must be able to {verb.lower()} {noun} through the interface",
#                 f"The system must provide {noun} {verb.lower()}ing capabilities",
#                 f"The application shall support the ability to {verb.lower()} {noun}"
#             ]
            
#             requirement = {
#                 "diagramId": element.get("diagramId"),
#                 "type": random.choice(requirement_types),
#                 "description": random.choice(templates),
#                 "priority": random.choice(priority_levels),
#                 "elementId": element.get("id")
#             }
            
#             requirements.append(requirement)
    
#     # Add some generic non-functional requirements
#     general_nfrs = [
#         "The system shall respond to user actions within 2 seconds",
#         "The system shall be available 99.9% of the time during business hours",
#         "User data must be encrypted using industry standard encryption methods",
#         "The system must be compatible with major web browsers",
#         "The user interface must be accessible following WCAG 2.1 standards"
#     ]
    
#     # Add 2-3 general non-functional requirements
#     for i in range(random.randint(2, 3)):
#         if elements:  # Make sure there's at least one element to get diagramId from
#             requirement = {
#                 "diagramId": elements[0].get("diagramId"),
#                 "type": "non-functional",
#                 "description": general_nfrs[i % len(general_nfrs)],
#                 "priority": random.choice(priority_levels),
#                 "elementId": None  # Not associated with a specific element
#             }
#             requirements.append(requirement)
    
#     return requirements

# def simulate_processing_delay(ms):
#     """Helper function to simulate processing delay"""
#     time.sleep(ms / 1000)
import os
import json
import numpy as np
from image_processor import image_processor
from ocr_processor import ocr_service
from nlp_processor import nlp_service
from estimation_service import effort_estimator

class DiagramProcessor:
    """
    Coordinates the processing pipeline for use case diagrams:
    1. Image Processing - Detect actors and use cases in the diagram
    2. OCR - Extract text from the detected regions
    3. NLP Processing - Generate requirements based on the extracted info
    4. Effort Estimation - Estimate effort, cost, and timeline
    """
    
    def __init__(self):
        # Define processing stages
        self.stages = [
            "image_processing",
            "ocr_processing",
            "nlp_processing",
            "requirements_generation",
            "effort_estimation"
        ]
    
    def process_diagram(self, diagram_id, image_path, callback=None):
        """
        Process a use case diagram through the entire pipeline
        
        Args:
            diagram_id: ID of the diagram 
            image_path: Path to the diagram image
            callback: Optional callback function to update progress
            
        Returns:
            Dictionary containing all processing results
        """
        results = {
            'diagram_id': diagram_id,
            'image_path': image_path,
            'stages': {}
        }
        
        # Create directory for debug images
        debug_dir = os.path.join(os.path.dirname(image_path), f"diagram_{diagram_id}_debug")
        os.makedirs(debug_dir, exist_ok=True)
        
        try:
            # Stage 1: Image Processing
            self._update_progress(callback, "image_processing", "started")
            image_results = image_processor.process_image(image_path)
            
            # Store actor and use case coordinates
            results['stages']['image_processing'] = {
                'status': 'completed',
                'actor_coordinates': image_results['actor_coordinates'],
                'use_case_coordinates': image_results['use_case_coordinates'],
                'debug_image': image_results.get('debug_image_path')
            }
            self._update_progress(callback, "image_processing", "completed")
            
            # Stage 2: OCR Processing
            self._update_progress(callback, "ocr_processing", "started")
            ocr_results = ocr_service.perform_ocr(
                image_path,
                image_results['actor_coordinates'],
                image_results['use_case_coordinates']
            )
            
            # Store actor and use case names
            results['stages']['ocr_processing'] = {
                'status': 'completed',
                'actor_names': ocr_results['actor_names'],
                'use_case_names': ocr_results['use_case_names'],
                'debug_image': ocr_results.get('debug_image_path')
            }
            self._update_progress(callback, "ocr_processing", "completed")
            
            # Stage 3: Detect connections between actors and use cases
            self._update_progress(callback, "nlp_processing", "started")
            connections = image_processor.detect_connections(
                image_path,
                image_results['actor_coordinates'],
                image_results['use_case_coordinates']
            )
            
            # Combine data to create actor and use case objects
            actors = []
            for i, coords in enumerate(image_results['actor_coordinates']):
                if i < len(ocr_results['actor_names']):
                    name = ocr_results['actor_names'][i]
                else:
                    name = f"Actor {i+1}"
                    
                actors.append({
                    'id': i + 1,
                    'name': name,
                    'type': 'Secondary' if 'system' in name.lower() else 'Primary',
                    'coordinates': coords,
                    'diagramId': diagram_id
                })
                
            use_cases = []
            for i, coords in enumerate(image_results['use_case_coordinates']):
                if i < len(ocr_results['use_case_names']):
                    name = ocr_results['use_case_names'][i]
                else:
                    name = f"Use Case {i+1}"
                    
                use_cases.append({
                    'id': i + 1,
                    'name': name,
                    'coordinates': coords,
                    'diagramId': diagram_id,
                    'description': '',
                    'complexity': 'Average'
                })
            
            results['stages']['nlp_processing'] = {
                'status': 'completed',
                'actors': actors,
                'use_cases': use_cases,
                'connections': connections
            }
            self._update_progress(callback, "nlp_processing", "completed")
            
            # Stage 4: Generate requirements
            self._update_progress(callback, "requirements_generation", "started")
            requirements = nlp_service.generate_requirements(use_cases, actors, connections)
            
            results['stages']['requirements_generation'] = {
                'status': 'completed',
                'requirements': requirements
            }
            self._update_progress(callback, "requirements_generation", "completed")
            
            # Stage 5: Estimate effort
            self._update_progress(callback, "effort_estimation", "started")
            estimation = effort_estimator.estimate_effort(use_cases, actors, requirements)
            
            results['stages']['effort_estimation'] = {
                'status': 'completed',
                'estimation': estimation
            }
            self._update_progress(callback, "effort_estimation", "completed")
            
            # Save full results for debugging/reference
            results_path = os.path.join(debug_dir, "processing_results.json")
            with open(results_path, 'w') as f:
             def convert_np(obj):
                if isinstance(obj, (np.integer, np.int64)):
                   return int(obj)
                if isinstance(obj, (np.floating, np.float64)):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return str(obj)



             json.dump(results, f, indent=2, default=convert_np)
            
            return {
                'actors': actors,
                'use_cases': use_cases,
                'requirements': requirements,
                'estimation': estimation,
                'debug_dir': debug_dir
            }
            
        except Exception as e:
            # Log the error and update progress
            import traceback
            error_message = f"Error in {self._get_current_stage(results)}: {str(e)}"
            error_details = traceback.format_exc()
            
            current_stage = self._get_current_stage(results)
            if current_stage:
                results['stages'][current_stage] = {
                    'status': 'error',
                    'error': error_message,
                    'details': error_details
                }
                self._update_progress(callback, current_stage, "error", error_message)
            
            # Save error results for debugging
            error_path = os.path.join(debug_dir, "processing_error.json")
            with open(error_path, 'w') as f:
                json.dump({
                    'error': error_message,
                    'details': error_details,
                    'results_so_far': results
                }, f, indent=2)
            
            raise Exception(error_message)
    
    def _update_progress(self, callback, stage, status, message=None):
        """Update processing progress via callback if provided"""
        if callback:
            callback(stage, status, message)
    
    def _get_current_stage(self, results):
        """Get the current processing stage based on results"""
        for stage in self.stages:
            if stage not in results['stages'] or results['stages'][stage]['status'] != 'completed':
                return stage
        return None

# Singleton instance
diagram_processor = DiagramProcessor()
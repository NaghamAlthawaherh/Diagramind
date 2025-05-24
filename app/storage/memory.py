<<<<<<< HEAD
import json
import datetime

class MemStorage:
    """
    In-memory storage implementation for the Use Case Analyzer application.
    This class provides temporary methods to store and retrieve users, diagrams,
    elements, requirements, estimations, and analysis sessions.
    """

    def __init__(self):  
        self.users = {}
        self.use_case_diagrams = {}
        self.diagram_elements = {}
        self.requirements = {}
        self.estimations = {}
        self.analysis_sessions = {}

        self.user_id = 0
        self.diagram_id = 0
        self.element_id = 0
        self.requirement_id = 0
        self.estimation_id = 0
        self.session_id = 0

    # User methods
    def get_user(self, id):
        return self.users.get(id)

    def get_user_by_username(self, username):
        for user in self.users.values():
            if user.get("username") == username:
                return user
        return None

    def create_user(self, user_data):
        self.user_id += 1
        user = {
            "id": self.user_id,
            **user_data
        }
        self.users[self.user_id] = user
        return user

    # Use Case Diagram methods
    def get_use_case_diagram(self, id):
        return self.use_case_diagrams.get(id)

    def create_use_case_diagram(self, diagram_data):
        self.diagram_id += 1
        diagram = {
            "id": self.diagram_id,
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
            **diagram_data
        }
        self.use_case_diagrams[self.diagram_id] = diagram
        return diagram

    def update_use_case_diagram(self, id, updates):
        diagram = self.use_case_diagrams.get(id)
        if diagram:
            diagram.update({
                **updates,
                "updatedAt": datetime.datetime.now().isoformat()
            })
            return diagram
        return None

    # Diagram Element methods
    def get_diagram_element(self, id):
        return self.diagram_elements.get(id)

    def get_diagram_elements_by_diagram_id(self, diagram_id):
        return [
            element for element in self.diagram_elements.values()
            if element.get("diagramId") == diagram_id
        ]

    def create_diagram_element(self, element_data):
        self.element_id += 1
        element = {
            "id": self.element_id,
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
            **element_data
        }
        self.diagram_elements[self.element_id] = element
        return element

    def update_diagram_element(self, id, updates):
        element = self.diagram_elements.get(id)
        if element:
            element.update({
                **updates,
                "updatedAt": datetime.datetime.now().isoformat()
            })
            return element
        return None

    # Requirements methods
    def get_requirement(self, id):
        return self.requirements.get(id)

    def get_requirements_by_diagram_id(self, diagram_id):
        return [
            req for req in self.requirements.values()
            if req.get("diagramId") == diagram_id
        ]

    def create_requirement(self, requirement_data):
        self.requirement_id += 1
        requirement = {
            "id": self.requirement_id,
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
            **requirement_data
        }
        self.requirements[self.requirement_id] = requirement
        return requirement

    # Estimation methods
    def get_estimation(self, id):
        return self.estimations.get(id)

    def get_estimation_by_diagram_id(self, diagram_id):
        for est in self.estimations.values():
            if est.get("diagramId") == diagram_id:
                return est
        return None

    def create_estimation(self, estimation_data):
        self.estimation_id += 1
        estimation = {
            "id": self.estimation_id,
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
            **estimation_data
        }
        self.estimations[self.estimation_id] = estimation
        return estimation

    # Analysis Session methods
    def get_analysis_session(self, id):
        return self.analysis_sessions.get(id)

    def get_analysis_session_by_diagram_id(self, diagram_id):
        for session in self.analysis_sessions.values():
            if session.get("diagramId") == diagram_id:
                return session
        return None

    def create_analysis_session(self, session_data):
        self.session_id += 1
        session = {
            "id": self.session_id,
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
            "startedAt": datetime.datetime.now().isoformat(),
            **session_data
        }
        self.analysis_sessions[self.session_id] = session
        return session

    def update_analysis_session(self, id, updates):
        session = self.analysis_sessions.get(id)
        if session:
            session.update({
                **updates,
                "updatedAt": datetime.datetime.now().isoformat()
            })
            return session
        return None

    def update_analysis_session_by_diagram_id(self, diagram_id, updates):
        session = self.get_analysis_session_by_diagram_id(diagram_id)
        if session:
            return self.update_analysis_session(session["id"], updates)
        return None
storage = MemStorage()
=======
import json
import datetime

class MemStorage:
    """
    In-memory storage implementation for the Use Case Analyzer application.
    This class provides temporary methods to store and retrieve users, diagrams,
    elements, requirements, estimations, and analysis sessions.
    """

    def __init__(self):  
        self.users = {}
        self.use_case_diagrams = {}
        self.diagram_elements = {}
        self.requirements = {}
        self.estimations = {}
        self.analysis_sessions = {}

        self.user_id = 0
        self.diagram_id = 0
        self.element_id = 0
        self.requirement_id = 0
        self.estimation_id = 0
        self.session_id = 0

    # User methods
    def get_user(self, id):
        return self.users.get(id)

    def get_user_by_username(self, username):
        for user in self.users.values():
            if user.get("username") == username:
                return user
        return None

    def create_user(self, user_data):
        self.user_id += 1
        user = {
            "id": self.user_id,
            **user_data
        }
        self.users[self.user_id] = user
        return user

    # Use Case Diagram methods
    def get_use_case_diagram(self, id):
        return self.use_case_diagrams.get(id)

    def create_use_case_diagram(self, diagram_data):
        self.diagram_id += 1
        diagram = {
            "id": self.diagram_id,
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
            **diagram_data
        }
        self.use_case_diagrams[self.diagram_id] = diagram
        return diagram

    def update_use_case_diagram(self, id, updates):
        diagram = self.use_case_diagrams.get(id)
        if diagram:
            diagram.update({
                **updates,
                "updatedAt": datetime.datetime.now().isoformat()
            })
            return diagram
        return None

    # Diagram Element methods
    def get_diagram_element(self, id):
        return self.diagram_elements.get(id)

    def get_diagram_elements_by_diagram_id(self, diagram_id):
        return [
            element for element in self.diagram_elements.values()
            if element.get("diagramId") == diagram_id
        ]

    def create_diagram_element(self, element_data):
        self.element_id += 1
        element = {
            "id": self.element_id,
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
            **element_data
        }
        self.diagram_elements[self.element_id] = element
        return element

    def update_diagram_element(self, id, updates):
        element = self.diagram_elements.get(id)
        if element:
            element.update({
                **updates,
                "updatedAt": datetime.datetime.now().isoformat()
            })
            return element
        return None

    # Requirements methods
    def get_requirement(self, id):
        return self.requirements.get(id)

    def get_requirements_by_diagram_id(self, diagram_id):
        return [
            req for req in self.requirements.values()
            if req.get("diagramId") == diagram_id
        ]

    def create_requirement(self, requirement_data):
        self.requirement_id += 1
        requirement = {
            "id": self.requirement_id,
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
            **requirement_data
        }
        self.requirements[self.requirement_id] = requirement
        return requirement

    # Estimation methods
    def get_estimation(self, id):
        return self.estimations.get(id)

    def get_estimation_by_diagram_id(self, diagram_id):
        for est in self.estimations.values():
            if est.get("diagramId") == diagram_id:
                return est
        return None

    def create_estimation(self, estimation_data):
        self.estimation_id += 1
        estimation = {
            "id": self.estimation_id,
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
            **estimation_data
        }
        self.estimations[self.estimation_id] = estimation
        return estimation

    # Analysis Session methods
    def get_analysis_session(self, id):
        return self.analysis_sessions.get(id)

    def get_analysis_session_by_diagram_id(self, diagram_id):
        for session in self.analysis_sessions.values():
            if session.get("diagramId") == diagram_id:
                return session
        return None

    def create_analysis_session(self, session_data):
        self.session_id += 1
        session = {
            "id": self.session_id,
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
            "startedAt": datetime.datetime.now().isoformat(),
            **session_data
        }
        self.analysis_sessions[self.session_id] = session
        return session

    def update_analysis_session(self, id, updates):
        session = self.analysis_sessions.get(id)
        if session:
            session.update({
                **updates,
                "updatedAt": datetime.datetime.now().isoformat()
            })
            return session
        return None

    def update_analysis_session_by_diagram_id(self, diagram_id, updates):
        session = self.get_analysis_session_by_diagram_id(diagram_id)
        if session:
            return self.update_analysis_session(session["id"], updates)
        return None
storage = MemStorage()
>>>>>>> 67ec19d3bb81bee2df6432acd2183c7468b661b9

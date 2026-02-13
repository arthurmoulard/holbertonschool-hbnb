**HBnB Technical Architecture Document**

**1. Introduction**

HBnB Evolution is a simplified AirBnB-like platform that enables user management, place listing, review submission, and amenity management. The system follows a three-layer architecture composed of the Presentation, Business Logic, and Persistence layers.
This documentation includes:
A high-level package diagram illustrating the layered architecture and facade pattern.


A detailed class diagram of the Business Logic layer.


Sequence diagrams showing interactions for key API operations.


The goal of this document is to clearly define the system structure, business rules, and data flow to ensure a consistent and maintainable implementation.

**2. Architectural Foundations**

The HBnB system follows a layered architecture pattern composed of the following layers:
Presentation Layer (API) – Handles HTTP requests and responses.


Business Logic Layer – Contains core application rules and orchestration logic.


Data Access Layer – Responsible for persistence and data retrieval.


A Facade Pattern is used to simplify communication between the API layer and the Business Logic layer. The API delegates processing to business services, which encapsulate validation, transformation, and coordination logic.
This separation of concerns improves:
Maintainability


Scalability


Testability



**2. High-Level Package Diagram**

HBnB Package Diagram Analysis
Overview
This diagram illustrates the three-tier layered architecture of the HBnB project, implementing clear separation of concerns across presentation, business logic, and data persistence layers.
Layer Structure
Presentation Layer
UI: User interface for end-user interactions
Presentation Logic: Data formatting and client-side validation
API: REST endpoints exposing application functionality
Purpose: Receives user requests, validates input, and forwards to business layer.
Business Logic Layer
Core domain entities:
User: User management and authentication
Place: Property/accommodation management
Review: User reviews and ratings
Amenity: Property features and services
Purpose: Implements business rules, validates operations, orchestrates entity interactions, and ensures data consistency.
Persistence Layer
DataBase: Data storage and retrieval system
Purpose: Abstracts data access and provides CRUD operations for business entities.
Key Design Decisions
Facade Pattern
The API layer acts as a simplified facade to complex business logic, providing a consistent interface to clients.
Unidirectional Dependencies
Dependencies flow top-down (Presentation → Business Logic → Persistence), ensuring lower layers remain independent of upper layers.
Separation of Concerns
Each layer has distinct responsibilities, enabling independent development, testing, and modification.
Benefits
Modularity: Independent layer development and testing
Reusability: Business logic accessible from multiple interfaces
Maintainability: Changes isolated to specific layers
Testability: Simplified unit and integration testing
Scalability: Independent layer scaling
Role in Project
This high-level architecture serves as the blueprint for organizing code structure, defining inter-layer interfaces, and maintaining architectural consistency throughout development.


<img width="322" height="630" alt="image" src="https://github.com/user-attachments/assets/06cd2b1c-2e23-4c90-8371-bf33aa9be595" />


**3. Detailed Class Diagram For Business Logic Layer**

Overview
This diagram details the core domain entities of the HBnB Business Logic Layer, showing attributes, methods, and relationships that implement business rules between the Presentation and Persistence layers.
Core Entities
User
Attributes: first_name, last_name, email, password (strings); id (bool)
Methods: register(), updated(), deleted()
Purpose: Manages authentication and serves as owner/author reference for places and reviews
Place
Attributes: title, description (strings); price, latitude, longitude (floats); user (User reference)
Methods: created(), updated(), deleted(), listed()
Purpose: Represents rental properties with geolocation for mapping and search. Linked to owner via User.
Review
Attributes: rating (float), comment (string); place (Place), user (User) references
Methods: created(), updated(), deleted(), listed()
Purpose: Manages property ratings and feedback. Dual relationships ensure accountability (User) and proper association (Place).
Amenity_Entity
Attributes: name, description (strings)
Methods: created(), updated(), deleted(), listed()
Purpose: Represents property features (WiFi, parking, etc.) enabling categorization and filtered searches


Role in Architecture
Translates business logic into database schemas, API contracts, and validation rules. Bridges API requests (above) with data persistence (below).


<img width="575" height="578" alt="image" src="https://github.com/user-attachments/assets/c9578065-35a2-4e55-a132-587949fb84f4" />


**4. Sequence Diagrams**

1. User Registration - POST /users

<img width="769" height="625" alt="image" src="https://github.com/user-attachments/assets/02b10a74-f3bb-477c-9407-be4e81ce3625" />


In this sequence diagram, a new user signs up for an account. The user sends their registration data to the API, which forwards it to the business logic layer. The business logic validates the input data and securely hashes the password. Once validated, it saves the user information to the database. The database confirms the user was created, and this confirmation travels back through the layers, returning a user object to the user with a 201 Created status.





2. Place Creation - POST /places

<img width="684" height="566" alt="image" src="https://github.com/user-attachments/assets/0687b860-d5b5-4d93-bd37-ee4a9ea3576e" />


In this sequence diagram, an authenticated user creates a new property listing. The user submits the place details to the API, which passes the data to the business logic layer. The business logic first verifies the user's identity to ensure they're authorized to create a listing. It then builds and validates the place entity before saving it to the database. Once the database confirms the place was created, this confirmation is sent back through all layers, returning the created place details to the user with a 201 Created status.



3. Review Submission - POST /reviews

<img width="762" height="611" alt="image" src="https://github.com/user-attachments/assets/2dabbe17-e581-422c-a75b-1c48dd7333d2" />


In this sequence diagram, a user submits a review for a property they've stayed at. The user sends their rating and comment to the API, which forwards it to the business logic layer. The business logic verifies that the place exists and that the user is eligible to review it. It then constructs the review entity with proper validation before saving it to the database. The database confirms the review was created, and this acknowledgment travels back through the layers, returning the review details to the user with a 201 Created status.



4. Fetching Places List - GET /places

<img width="868" height="530" alt="image" src="https://github.com/user-attachments/assets/fffbf098-39bf-43fe-88c1-592467b2d51b" />


In this sequence diagram, a user searches for available places. The user sends a request with optional search filters to the API, which asks the business logic layer to retrieve the matching data. The business logic queries the database for places that meet the criteria. Once the data is found, it's returned from the database as a list of places. The business logic transforms this into a presentation-friendly format and sends it back through the API to the user with a 200 OK status.


**Conclusion:**

The HBnB architecture, organized into three layers (Presentation, Business Logic, Persistence) with a Facade pattern, ensures a clear separation of responsibilities. The package, class, and sequence diagrams illustrate the key entities and data flows, ensuring maintainability, scalability, and testability. This document serves as a solid reference for the development and future evolution of the platform.


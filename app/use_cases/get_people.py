from entities.person import Person

class GetPeopleUseCase:
    def __init__(self, people_repository, logger):
        self.people_repository = people_repository
        self.logger = logger

    def get_people_by_page(self, page: int):
        self.logger.info(f"Fetching people from page {page}")
        page_data = self.people_repository.get_people(page)
        return page_data["results"], page_data["next"]

    def validate_results(self, results: list): 
        self.logger.info("Validating results after fetching people")
        # Verify the type of the results and make sure that it is a list of dictionaries
        if isinstance(results, list) and all(isinstance(person, dict) for person in results):
            # Transform data into Person objects
            people = [Person(**person) for person in results]
            return people
        else:
            error_message = "Some of the data provided is not valid"
            self.logger.error(error_message)
            raise TypeError(error_message)

    def sort_people(self, people: list):
        self.logger.info("Sorting results by name in ascending order")
        return sorted(people, key=lambda p: p.name)

    def get_people(self, page: int):
        results, next_page = self.get_people_by_page(page)

        people = self.validate_results(results)

        # Sort people by name
        sorted_people = self.sort_people(people)

        return sorted_people
        
    def get_all_people(self):
        all_people = []
        page = 1

        while True:
            results, next_page = self.get_people_by_page(page)

            people = self.validate_results(results)
            
            all_people.extend(people)
            # If there is next page, increment the counter
            if next_page is not None:
                page += 1
            else:
                break
        # Sort people by name
        sorted_people = self.sort_people(all_people)
        return sorted_people
        
    def execute(self, page: int = None):
        self.logger.info("Executing use case to get people")
        if page:
            return self.get_people(page)
        else:
            return self.get_all_people()



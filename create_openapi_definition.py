from itsm_api import views
import yaml
import datetime


resources_list = [
    # Root-level resource
    views.Root,
    # Top-level list resources
    views.UserList,
    # views.CustomerList,
    # views.TicketList,
    # views.CommentList,
    # views.CustomerUserAssociationList,
    # # Individual resources
    # views.User,
    # views.Customer,
    # views.Ticket,
    # views.Comment,
    # views.CustomerUserAssociation,
    # # Second-level list resources
    # views.UserCustomerList,
    # views.CustomerUserList,
    # views.CustomerTicketList,
    # views.UserTicketList
]

# Base document definition. Contains metadata such as OpenAPI document version, API
# information, along with the outline for filling in the API endpoint information.
openapi_definition = {
    "openapi": "3.0.1",
    "info": {
        "title": "Aportio ITSM REST API reference",
        "description": "Reference documentation for Aportio's ITSM REST API.",
        "version": "0.1"
    },
    "tags": [
        {
            "name": "Root",
            "description": "The root level of the API"
        },
        {
            "name": "Users",
            "description": "Requests against user resources"
        },
        {
            "name": "Tickets",
            "description": "Requests against ticket resources"
        }
    ],
    "paths": {
    }
}


def add_get_definition(resource):
    # Get the path to the resource. This will be used as a key in the definition dict.
    path = resource.URL

    if not openapi_definition["paths"].get(path):
        openapi_definition["paths"][path] = {}

    # Get the OpenAPI definition from the resource's GET method docstring, and use pyyaml to
    # load it into python.
    get_resource_definition_yaml = resource._get.__doc__.split('---')[-1]
    get_resource_definition      = yaml.load(get_resource_definition_yaml)

    # Update the main OpenAPI definition with the resource's GET method.
    openapi_definition["paths"][path]["get"] = get_resource_definition


def add_post_definition(resource):
    # Get the path to the resource. This will be used as a key in the definition dict.
    path = resource.URL

    if not openapi_definition["paths"].get(path):
        openapi_definition["paths"][path] = {}

    # Get the OpenAPI definition from the resource's GET method docstring, and use pyyaml to
    # load it into python.
    post_resource_definition_yaml = resource._post.__doc__.split('---')[-1]
    post_resource_definition      = yaml.load(post_resource_definition_yaml)

    # Update the main OpenAPI definition with the resource's GET method.
    openapi_definition["paths"][path]["post"] = post_resource_definition


if __name__ == "__main__":
    # Go through the list of resources that we want to create definitions for.
    for res in resources_list:
        # If the resource has a GET method, add that to the definition.
        if "_get" in dir(res):
            add_get_definition(res)

        # If the resource has a POST method, add that to the definition.
        if "_post" in dir(res):
            add_post_definition(res)

    # Get the date and time for now and generate a name for the definition file
    now = datetime.datetime.now()
    filename = f"Aportio REST API definition {now}"

    # Save the definition to the definition file
    with open(f"{filename}.yaml", "w") as definition_file:
        yaml.dump(openapi_definition, definition_file, sort_keys=False)

    print(f"Wrote OpenAPI definition to {filename}")
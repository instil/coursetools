# Listing and managing projects on codebase

We use [codebase](https://www.codebasehq.com/) for managing our courses.

Each course gets a project, and each project gets one or more git repos to hold
course materials (this application currently generates the material for those
git repos but it doesn't interact with codebase yet).

This task is to connect to codebase via the codebase api and manage projects.

The API documentation is here: https://support.codebasehq.com/kb

There's an API key stored in ~/.codebase/credentials.toml

Here's the steps to get going. 

1. add a cli entrypoint for listing projects, use `-p` and `--project` as the 
   argument - print "listing projects" initially
2. connect to codebase and list projects. show only active projects
3. allow adding `--all` as an argument to list all projects including archived ones

The API documentation for projects is https://support.codebasehq.com/kb/projects
The auth documentation is on https://support.codebasehq.com/kb

## Step-by-Step Implementation Plan

### Conditions
1. use a new package called `codebase` for code here
2. code in course tools can be used if necessary - look for opportunities to 
   practice DRY principles
3. Use TDD and take small steps - avoid using too many mocks
4. Tests should avoid connecting directly with codebase. You may need to save
   live data as fixture data for test mocks. There is already a fixture in place
   for the projects api call
5. Only unit tests are required; no integration-style tests are needed
6. The API uses XML only, no support for JSON

### Phase 1: Setup and Configuration
1. **Read credentials file**
   - Load `~/.codebase/credentials.toml` to get API key and account details
   - Parse TOML format to extract necessary authentication info

2. **Review API documentation**
   - Check authentication requirements (likely API key in headers)
   - Identify the projects list endpoint and response format
   - Understand filtering options for active vs archived projects

### Phase 2: CLI Interface
3. **Add CLI command**
   - Create new command/subcommand for project listing
   - Add `-p` and `--project` flags (determine if these are for filtering or action)
   - Add `--all` flag for including archived projects
   - Initial implementation prints "listing projects"

4. **Add argument parsing**
   - Use existing CLI framework (likely argparse or click)
   - Define help text and argument descriptions
   - Handle flag combinations appropriately

### Phase 3: API Integration
5. **Create API client module**
   - Implement authentication using API key from credentials
   - Create base HTTP client with proper headers
   - Add error handling for network/auth failures

6. **Implement projects list endpoint**
   - Make GET request to projects API endpoint
   - Parse JSON response
   - Filter for active projects by default
   - Include archived when `--all` flag is present

### Phase 4: Output Formatting
7. **Format and display results**
   - Display project names, IDs, and relevant metadata
   - Use clean, readable output format (table or list)
   - Handle empty results gracefully

### Phase 5: Testing and Refinement
8. **Test the implementation**
   - Test with valid credentials
   - Test `--all` flag behavior
   - Test error cases (invalid credentials, network issues)
   - Verify filtering works correctly

9. **Add documentation**
   - Update README if needed
   - Add inline code comments for complex logic
   - Document the command usage


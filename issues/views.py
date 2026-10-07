import json
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Reporter, Issue, CriticalIssue, LowPriorityIssue


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


REPORTERS_FILE = os.path.join(BASE_DIR, "reporters.json")
ISSUES_FILE = os.path.join(BASE_DIR, "issues.json")


def get_reporters_file_path():
    return REPORTERS_FILE


def get_issues_file_path():
    return ISSUES_FILE


@csrf_exempt
def reporters(request):

    if request.method == "POST":

        data = json.loads(request.body)

        reporter = Reporter(
            data["id"],
            data["name"],
            data["email"],
            data["team"]
        )

        reporter.validate()

        file_path = get_reporters_file_path()

        with open(file_path, "r") as f:
            reporters_data = json.load(f)

        reporters_data.append(reporter.to_dict())

        with open(file_path, "w") as f:
            json.dump(reporters_data, f, indent=4)

        return JsonResponse(
            reporter.to_dict(),
            status=201
        )

    elif request.method == "GET":

        file_path = get_reporters_file_path()

        with open(file_path, "r") as f:
            reporters_data = json.load(f)

        return JsonResponse(
            reporters_data,
            safe=False,
            status=200
        )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )
    
@csrf_exempt
def reporter_detail(request, reporter_id):

    file_path = get_reporters_file_path()

    with open(file_path, "r") as f:
        reporters_data = json.load(f)

    # GET a single reporter
    if request.method == "GET":

        for reporter in reporters_data:
            if reporter["id"] == reporter_id:
                return JsonResponse(reporter, status=200)

        return JsonResponse(
            {"error": "Reporter not found"},
            status=404
        )

    # UPDATE a reporter
    elif request.method == "PUT":

        data = json.loads(request.body)

        for reporter in reporters_data:

            if reporter["id"] == reporter_id:

                reporter["name"] = data["name"]
                reporter["email"] = data["email"]
                reporter["team"] = data["team"]

                updated_reporter = Reporter(
                    reporter["id"],
                    reporter["name"],
                    reporter["email"],
                    reporter["team"]
                )

                updated_reporter.validate()

                with open(file_path, "w") as f:
                    json.dump(
                        reporters_data,
                        f,
                        indent=4
                    )

                return JsonResponse(
                    updated_reporter.to_dict(),
                    status=200
                )

        return JsonResponse(
            {"error": "Reporter not found"},
            status=404
        )
    
    elif request.method == "DELETE":

        for reporter in reporters_data:

            if reporter["id"] == reporter_id:

                reporters_data.remove(reporter)

                with open(file_path, "w") as f:
                    json.dump(
                        reporters_data,
                        f,
                        indent=4
                    )

                return JsonResponse(
                    {
                        "message": "Reporter deleted successfully"
                    },
                    status=200
                )

        return JsonResponse(
            {"error": "Reporter not found"},
            status=404
        )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )
    

@csrf_exempt
def issues(request):

    # =========================
    # POST - Create an issue
    # =========================

    if request.method == "POST":

        try:
            data = json.loads(request.body)

            issue_id = data["id"]
            title = data["title"]
            description = data["description"]
            status = data["status"]
            priority = data["priority"]
            reporter_id = data["reporter_id"]

        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=400
            )

        except KeyError as e:
            return JsonResponse(
                {"error": f"Missing field: {e.args[0]}"},
                status=400
            )

        # Create the correct Issue subclass
        if priority == "critical":

            issue = CriticalIssue(
                issue_id,
                title,
                description,
                status,
                priority,
                reporter_id
            )

        elif priority == "low":

            issue = LowPriorityIssue(
                issue_id,
                title,
                description,
                status,
                priority,
                reporter_id
            )

        else:

            issue = Issue(
                issue_id,
                title,
                description,
                status,
                priority,
                reporter_id
            )

        # Validate issue
        try:
            issue.validate()

        except ValueError as e:
            return JsonResponse(
                {"error": str(e)},
                status=400
            )

        # Read issues.json
        file_path = get_issues_file_path()

        with open(file_path, "r") as f:
            issues_data = json.load(f)

        # Add new issue
        issues_data.append(issue.to_dict())

        # Save back to issues.json
        with open(file_path, "w") as f:
            json.dump(
                issues_data,
                f,
                indent=4
            )

        # Prepare response
        response_data = issue.to_dict()

        response_data["message"] = issue.describe()

        return JsonResponse(
            response_data,
            status=201
        )

    # =========================
    # GET - Retrieve issues
    # =========================

    elif request.method == "GET":

        file_path = get_issues_file_path()

        with open(file_path, "r") as f:
            issues_data = json.load(f)

        issue_id = request.GET.get("id")
        status = request.GET.get("status")

    # GET issue by ID
        if issue_id:

            issue_id = int(issue_id)

            for issue in issues_data:

                if issue["id"] == issue_id:

                    return JsonResponse(
                    issue,
                    status=200
                    )

            return JsonResponse(
            {"error": "Issue not found"},
            status=404
            )

    # GET issues by status
        if status:

            filtered_issues = []

            for issue in issues_data:

                if issue["status"] == status:

                    filtered_issues.append(issue)

            return JsonResponse(
            filtered_issues,
            safe=False,
            status=200
            )

    # GET all issues
        return JsonResponse(
            issues_data,
            safe=False,
            status=200
        )
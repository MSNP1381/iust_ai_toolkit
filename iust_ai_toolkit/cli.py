import csv
import json
import os
import pkgutil

import click

from iust_ai_toolkit.abdi_4031 import DecisionTreeSubmission, submit_notebook


@click.group()
def main():
    """IUST AI Toolkit CLI"""
    pass


@main.command()
def list_courses():
    """List available courses (modules) in the IUST AI Toolkit."""
    courses = [name for _, name, is_pkg in pkgutil.iter_modules(["iust_ai_toolkit"]) if is_pkg]
    click.echo("Available Courses:")
    for course in courses:
        click.echo(f"- {course}")


@main.command()
@click.option("--course", required=True, help="Course name to list assignments for")
def list_assignments(course):
    """List assignments for a specific course."""
    try:
        module = __import__(f"iust_ai_toolkit.{course}", fromlist=[""])
        assignments = [name for _, name, is_pkg in pkgutil.iter_modules(module.__path__) if is_pkg]
        click.echo(f"Assignments for {course}:")
        for assignment in assignments:
            click.echo(f"- {assignment}")
    except ImportError:
        click.secho(f"Error: Course '{course}' not found.", fg="red", bold=True)


@main.command()
@click.option("--student-id", required=True, help="Student ID")
@click.option("--notebook-path", default="./main.ipynb", help="Path to the notebook file")
@click.option("--project", default="decision-tree", help="Project name (default: decision-tree)")
def submit(student_id, notebook_path, project):
    """Submit an assignment"""
    click.echo(f"Submitting {project} assignment for student {student_id}")
    if project == "decision-tree":
        submit_notebook(student_id, notebook_path)
    else:
        click.echo(f"Project {project} is not supported yet.")
    click.echo("Submission complete!")


@main.command()
@click.option("--directory", required=True, help="Directory containing submission zip files")
@click.option("--output", default="comparison_report.csv", help="Output CSV file name")
@click.option("--verbose", is_flag=True, help="Generate verbose output")
def compare_submissions(directory, output, verbose):
    """Compare multiple submissions and generate a report"""
    if not DecisionTreeSubmission.is_ta_version_installed():
        click.secho(
            "Error: TA version is not installed. Please install iust_ai_toolkit[ta] to use this feature.",
            fg="red",
            bold=True,
        )
        return

    authenticator = DecisionTreeSubmission(directory)
    submissions = [f for f in os.listdir(directory) if f.endswith("-decision_tree_submission.zip")]

    click.secho(f"Found {len(submissions)} submissions to compare.", fg="cyan")

    try:
        with click.progressbar(length=len(submissions), label="Analyzing submissions") as bar:
            results, verbose_results, ignore_cheating = authenticator.analyze_all_submissions(
                submissions, progress_callback=lambda: bar.update(1)
            )
    except ImportError as e:
        click.secho(f"Error: {str(e)}", fg="red", bold=True)
        return

    with open(output, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Student 1", "Student 2", "Similarity", "Potential Cheating"])
        for result in results:
            potential_cheating = (
                "Ignored"
                if ignore_cheating
                else ("Yes" if result[2] > authenticator.cheating_threshold else "No")
            )
            writer.writerow(result + (potential_cheating,))

    click.secho(f"Comparison report saved to {output}", fg="green")
    if ignore_cheating:
        click.secho(
            "Note: Potential cheating has been ignored due to high similarity across many submissions.",
            fg="yellow",
        )

    if verbose:
        verbose_output = output.rsplit(".", 1)[0] + "_verbose.json"
        with open(verbose_output, "w") as jsonfile:
            json.dump(verbose_results, jsonfile, indent=2)
        click.secho(f"Verbose comparison report saved to {verbose_output}", fg="green")

    # Print summary
    total_comparisons = len(results)
    potential_cheating_count = sum(1 for r in results if r[2] > authenticator.cheating_threshold)

    click.echo("\nSummary:")
    click.secho(f"Total comparisons: {total_comparisons}", fg="cyan")
    click.secho(
        f"Potential cheating cases: {potential_cheating_count}",
        fg="yellow" if potential_cheating_count > 0 else "green",
    )
    click.secho(f"Cheating threshold: {authenticator.cheating_threshold:.2f}", fg="cyan")


if __name__ == "__main__":
    main()

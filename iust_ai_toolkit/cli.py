import click
import os
import csv
import json
from .abdi_4031.decision_tree_submission import authenticate_notebook, DecisionTreeAuthenticator

@click.group()
def main():
    """IUST AI Toolkit CLI"""
    pass

@main.command()
@click.option('--student-id', required=True, help='Student ID')
@click.option('--notebook-path', default='./main.ipynb', help='Path to the notebook file')
@click.option('--project', default='decision-tree', help='Project name (default: decision-tree)')
def submit(student_id, notebook_path, project):
    """Submit an assignment"""
    click.echo(f"Submitting {project} assignment for student {student_id}")
    if project == 'decision-tree':
        authenticate_notebook(student_id, notebook_path)
    else:
        click.echo(f"Project {project} is not supported yet.")
    click.echo("Submission complete!")

@main.command()
@click.option('--directory', required=True, help='Directory containing submission zip files')
@click.option('--output', default='comparison_report.csv', help='Output CSV file name')
@click.option('--verbose', is_flag=True, help='Generate verbose output')
def compare_submissions(directory, output, verbose):
    """Compare multiple submissions and generate a report"""
    if not DecisionTreeAuthenticator.is_ta_version_installed():
        click.echo("Error: TA version is not installed. Please install iust_ai_toolkit[ta] to use this feature.")
        return

    authenticator = DecisionTreeAuthenticator(directory)
    submissions = [f for f in os.listdir(directory) if f.endswith('-decision_tree_submission.zip')]
    
    try:
        results, verbose_results, ignore_cheating = authenticator.analyze_all_submissions(submissions)
    except ImportError as e:
        click.echo(f"Error: {str(e)}")
        return
    
    with open(output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Student 1', 'Student 2', 'Similarity', 'Potential Cheating'])
        for result in results:
            potential_cheating = "Ignored" if ignore_cheating else ("Yes" if result[2] > authenticator.cheating_threshold else "No")
            writer.writerow(result + (potential_cheating,))
    
    click.echo(f"Comparison report saved to {output}")
    if ignore_cheating:
        click.echo("Note: Potential cheating has been ignored due to high similarity across many submissions.")

    if verbose:
        verbose_output = output.rsplit('.', 1)[0] + '_verbose.json'
        with open(verbose_output, 'w') as jsonfile:
            json.dump(verbose_results, jsonfile, indent=2)
        click.echo(f"Verbose comparison report saved to {verbose_output}")

if __name__ == '__main__':
    main()
from app.services.github_service import(
    get_github_profile,
    get_user_repositories
)

from app.services.analyzer_service import (
    extract_repo_data
)

from app.services.ai_service import (
    generate_summary,
    analyze_readme
)

from app.services.github_service import (
    clean_profile_data,
    get_readme
)

username = "Wajid0005"

profile = get_github_profile(username)
cleaned_profile = clean_profile_data(profile)
repos = get_user_repositories(username)

cleaned_data = extract_repo_data(repos)
readme = get_readme(
        "Wajid0005",
        "Calculate_my_package"
)
print(cleaned_profile)
print("----------------------------------")
print(repos[:2])
print("---------------------------------------------------")
for repo in cleaned_data[:5]:
    print(repo)

print("--------------------------------------------------------------------")

ai_response = generate_summary(cleaned_data[:3])
#print("README CONTENT:")
#print(readme)
print(ai_response)
print("-------------------------------------------------------------------------------")
readme_analysis = analyze_readme(readme)
print(readme_analysis)
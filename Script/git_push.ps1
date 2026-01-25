param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

git status
git add .

git commit -m "$Message"

git push
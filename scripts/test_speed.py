import subprocess

result = subprocess.run(
    ["speedtest"],
    capture_output=True,
    text=True
)

print(result.stdout)
print(result.stderr)

- https://github.com/ComplianceAsCode/content
- 
```bash
sudo apt install libopenscap8

wget https://github.com/ComplianceAsCode/content/releases/download/v0.1.66/scap-security-guide-0.1.66.zip

unzip -q scap-security-guide-0.1.66.zip
```

```bash
sudo oscap xccdf generate guide \

--profile xccdf_org.ssgproject.content_profile_stig \

scap-security-guide-0.1.60/ssg-ubuntu2004-ds.xml \

> rahasak-checklist.html
```

```bash
sudo oscap xccdf generate fix \

--fetch-remote-resources \

--fix-type ansible \

--result-id "" \

rahasak-result.xml > rahasak-playbook.yml
```
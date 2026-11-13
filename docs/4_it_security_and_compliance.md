# Apex Global Technologies — Information Security, Privacy & Compliance Policy

## 1. Password Security & Access Control Standards
To protect company infrastructure, intellectual property, and client information, all employees must comply with corporate access policies:
- **Password Length & Complexity**: All domain accounts require a minimum password length of **16 characters**, containing uppercase letters, lowercase letters, numbers, and symbols. Passwords must not contain personal names, birthdays, or dictionary words.
- **Enterprise Password Manager**: Employees are issued enterprise licenses for **1Password**. Passwords must be randomly generated and stored within the vault. Writing passwords on physical notes or in unencrypted text files is a critical compliance violation.
- **Mandatory Multi-Factor Authentication (MFA)**: Hardware security keys (YubiKey) or push notification authenticator apps (Okta Verify / Duo) are mandatory for all logins. SMS-based 2FA is deprecated and blocked due to SIM-swapping vulnerabilities.
- **Session Timeouts**: Corporate laptop screens must automatically lock after **5 minutes of inactivity**.

---

## 2. Data Classification & Handling Standards
Apex classifies company and customer data into four security tiers:
1. **Public (Tier 1)**: Marketing collaterals, published blog posts, press releases, public documentation. No handling restrictions.
2. **Internal (Tier 2)**: All-hands presentation slides, internal engineering wikis, product roadmaps. Shareable within Apex only.
3. **Confidential (Tier 3)**: Employee compensation data, financial forecasts, unannounced commercial contracts, and vendor agreements. Restricted to authorized departments.
4. **Restricted (Tier 4)**: Customer Personally Identifiable Information (PII), payment card information, production database backups, API master secret keys, and cryptographic certificates. Strict zero-trust access with role-based access control (RBAC) and audit logging.

---

## 3. Compliance Frameworks: SOC 2, ISO 27001 & GDPR
- **SOC 2 Type II Compliance**: Apex completes annual third-party SOC 2 Type II audits across Security, Availability, and Confidentiality trust principles.
- **GDPR & Privacy Regulations**: European customer data must be retained exclusively within EU-based data centers (Frankfurt / Dublin). The Data Protection Officer (DPO) can be reached at `privacy@apexglobal.internal`.
- **Right to Erasure (GDPR Article 17)**: Formal customer deletion requests must be acknowledged within 48 hours and fully executed across active production databases and backup replicas within **30 calendar days**.

---

## 4. Hardware Management & BYOD Restrictions
- **Company Hardware**: Production code development, client data access, and corporate cloud administration must occur strictly on managed corporate MacBooks or ThinkPads configured with **Jamf Pro / Intune MDM** and full-disk encryption (FileVault / BitLocker).
- **Bring Your Own Device (BYOD)**: Personal laptops are strictly barred from connecting to internal production networks, Kubernetes clusters, and corporate GitHub repositories. Personal mobile phones may access email and Slack only after installing the company's enterprise mobile management profile.

---

## 5. Security Incident Reporting & Escalation Protocol
- Any suspected security anomaly, lost laptop, phishing click, credential leak, or unexpected database query pattern must be reported immediately:
  - **Immediate Slack Notification**: Post in `#it-security-urgent`.
  - **Emergency Hotline / Email**: `security@apexglobal.internal` (triggers automated PagerDuty alarm to the SecOps On-Call Engineer).
- **Response SLA**: The SecOps Incident Commander initiates triage and containment within **15 minutes** of report receipt.

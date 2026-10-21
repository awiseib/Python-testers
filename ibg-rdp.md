# Technical Whitepaper: TWS/IB Gateway 10.50 Java Upgrade — Impact on Remote Desktop Authentication Workflows

**Interactive Brokers LLC**
**Document Classification:** Client Advisory
**Version:** 1.0
**Date:** October 21, 2026

---

## Executive Summary

With the release of Trader Workstation (TWS) and IB Gateway version 10.50, Interactive Brokers has upgraded the underlying Java Runtime Environment from Java 17 to Java 25. This upgrade brings improved performance, security, and long-term platform stability. However, it has introduced a known side effect for users who run IB Gateway or TWS on remote Windows servers accessed via Remote Desktop Protocol (RDP): the platform's automated reauthentication process may fail to complete successfully when the RDP session is disconnected in the standard manner.

This document outlines the technical background of the issue, its impact on affected users, and a documented workaround involving the Windows `tscon` command. As with all custom remote-access configurations, this workaround is provided for informational purposes only and is not covered under standard IB Client Services support.

---

## Background: Java 17 to Java 25 Migration

Beginning with TWS/IB Gateway 10.50, Interactive Brokers migrated the platform's Java runtime from Java 17 (LTS) to Java 25 (LTS). This update aligns IBKR's desktop trading applications with current Java security patches, performance improvements, and garbage collection enhancements, and ensures continued compatibility with modern operating system libraries.

As part of this migration, changes were made to how the Java Virtual Machine manages windowing, session, and authentication-related processes — specifically those tied to the platform's **auto-restart** feature, which periodically re-authenticates a running session without requiring the user to manually log in.

---

## Issue Description

### Root Cause

The IB Gateway and TWS auto-restart functionality depends on access to an active graphical session context to complete the reauthentication handshake (including rendering of the two-factor authentication prompt, session token refresh, and internal UI validation checks).

Under Java 17, this process was tolerant of certain "headless" or GUI-detached states that commonly occur when a Windows RDP session is disconnected normally (i.e., the user closes the RDP window via the "X" button or selects **Start > Disconnect**). Windows, by default, suspends the graphical session (Session ID) when an RDP connection is closed this way, effectively detaching it from any active console rendering context.

Under Java 25, this same detached-session state is handled differently by the JVM's windowing subsystem. As a result, when IB Gateway's auto-restart process attempts to reauthenticate while the GUI session is suspended (post-RDP-disconnect), the reauthentication handshake fails, and the platform does not successfully resume trading connectivity. In practice, this presents to the user as a connectivity drop that does not self-heal, requiring a manual relaunch and login.

### Affected Configurations

This issue has been observed specifically in the following scenario:

- IB Gateway or TWS 10.50 (or later) is running on a **Windows-based remote server** (physical or virtual).
- The server is accessed via **Remote Desktop Protocol (RDP)**.
- The RDP session is **disconnected** (not logged off) using standard Windows RDP disconnect methods.
- The platform's **auto-restart** feature is enabled and a scheduled reauthentication cycle occurs while the session is in a disconnected state.

Local desktop installations with an active, persistent GUI session (i.e., no RDP session detachment) are not affected by this issue.

---

## Workaround: Maintaining an Active Console Session via `tscon`

Users running IB Gateway on a Windows remote server may avoid triggering the GUI-detachment condition by using the Windows built-in `tscon` (Terminal Services Connection) utility to reattach the RDP session to the local console session **prior to disconnecting**, rather than disconnecting through the standard RDP interface.

### Procedure

1. Open a Command Prompt (or PowerShell) session on the remote Windows server with administrative privileges.
2. Identify the active RDP session ID using:
   ```
   query user
   ```
   This will return a session ID (commonly, but not always, session `2`) associated with the active RDP connection.
3. Run the following command to reattach that session to the local console, preserving an active graphical desktop state even after the RDP client disconnects:
   ```
   tscon 2 /dest:console
   ```
   *(Replace `2` with the actual session ID identified in Step 2.)*
4. The RDP client window will close automatically. However, because the session has been transferred to the console rather than suspended, the graphical environment — and consequently, the IB Gateway auto-restart authentication process — remains active and uninterrupted.

### Why This Works

The `tscon` command avoids the GUI-suspension state entirely by binding the session to the server's console session rather than leaving it in the disconnected RDP state that Java 25's windowing subsystem fails to handle correctly during reauthentication. Because the graphical desktop is technically never "disconnected" from a rendering context, IB Gateway's auto-restart process can complete its reauthentication handshake normally.

---

## Disclaimer

Interactive Brokers platforms — including TWS and IB Gateway — are designed, tested, and supported exclusively for environments that maintain an active graphical user interface (GUI). IBKR does not design, test, or certify its software for headless, virtualized-display-suspended, or session-detached server configurations.

The workaround described in this document, including use of the `tscon` command, involves modification of native Windows session behavior outside the scope of Interactive Brokers' platform. This information is provided **solely as a courtesy reference** for clients who choose to operate IB Gateway or TWS in custom remote server environments.

**Clients who implement this or any similar workaround do so entirely at their own discretion and risk.** Interactive Brokers:

- Does not guarantee the continued functionality of this workaround in future Windows updates or TWS/IB Gateway releases.
- Does not provide technical support, troubleshooting, or guidance for custom remote access configurations through Client Services.
- Recommends that institutional or high-availability users consult with their own IT infrastructure teams to validate the security and operational implications of maintaining console sessions in this manner, including potential impacts on Windows licensing terms for concurrent RDP sessions.

---

## Recommendations

1. **Evaluate necessity:** Where possible, consider running IB Gateway on infrastructure with a persistent, non-RDP-dependent graphical session (e.g., a dedicated always-on display or supported virtual display solution).
2. **Test thoroughly:** If implementing the `tscon` workaround, test the full auto-restart and reauthentication cycle in a non-production environment before relying on it for live trading.
3. **Monitor for updates:** Interactive Brokers continues to evaluate the Java 25 windowing behavior and may release platform updates that address the underlying auto-restart/GUI-detachment issue directly. Clients should keep TWS/IB Gateway updated to the latest available version.
4. **Maintain fallback monitoring:** Regardless of workaround implementation, clients should maintain independent monitoring/alerting for connectivity loss on any unattended trading infrastructure.

---

## Conclusion

The Java 17 to Java 25 upgrade in TWS/IB Gateway 10.50 improves the long-term stability and security posture of Interactive Brokers' desktop platforms but introduces a known limitation for GUI-detached remote sessions, such as those used in standard RDP disconnect workflows. The `tscon /dest:console` approach offers a practical, field-tested workaround for clients operating in Windows remote server environments. However, this solution falls outside the bounds of IBKR's standard platform support model, and clients implementing it should do so with a full understanding of the associated risks and support limitations outlined above.

For questions regarding supported platform configurations, please contact Interactive Brokers Client Services. For questions regarding custom remote server implementations, clients are encouraged to consult their internal IT resources or systems administrators.


---


# Security Addendum: Risk Considerations for the `tscon /dest:console` Workaround

**Interactive Brokers LLC**
**Document Classification:** Client Advisory — Security Supplement
**Version:** 1.0
**Date:** October 21, 2026

---

## Purpose

This addendum supplements the prior whitepaper on the TWS/IB Gateway 10.50 Java 25 upgrade and the associated `tscon 2 /dest:console` workaround. While the command addresses a functional reauthentication issue, clients should be aware that this technique carries **non-trivial security implications** that are independent of Interactive Brokers' platform and stem entirely from native Windows session management behavior. This section outlines those considerations for risk, compliance, and IT security teams evaluating whether to adopt this workaround.

---

## 1. Authentication Bypass on Session Reattachment

The `tscon` command can, under certain privilege conditions, reattach a disconnected session to the console **without requiring the invoking user to re-enter credentials** for that session. This is a well-documented Windows session-hijacking technique (publicly discussed in security research as early as 2017–2019) and has been cataloged as an adversary technique under privilege escalation / lateral movement frameworks (e.g., MITRE ATT&CK-aligned behaviors).

**Risk:** If executed by an account with sufficient rights (particularly `SYSTEM`-level access obtained via tools such as `PsExec -s` or a scheduled task), `tscon` can be used to seize control of **another user's active or disconnected session** — including sessions belonging to higher-privileged accounts — without supplying that user's password.

**Relevance to IBKR deployment:** Any server running IB Gateway that is reachable by multiple administrators, support staff, or scheduled/service accounts introduces a scenario where one party could access another's authenticated trading session without their knowledge or consent.

---

## 2. Bypassing the Default Windows Lock-on-Disconnect Behavior

When an RDP session is disconnected using the standard Windows mechanism, Windows typically locks the console desktop (if a user is logged in) or suspends the session entirely, requiring credentials to resume. Reattaching via `tscon` to the console **can leave the desktop unlocked and fully visible** to anyone with physical or console (e.g., KVM, IPMI, hypervisor console) access to the machine.

**Risk:** An unattended, unlocked desktop running IB Gateway with an active trading session exposes:
- Account balances, open positions, and order entry screens
- Live trading functionality to anyone with local/physical/console access
- Potential exposure to shoulder-surfing or opportunistic misuse in shared data center or shared-access environments

---

## 3. Elevated Privilege Requirement

Successful use of `tscon` to reattach a session not owned by the current user generally requires **administrative or SYSTEM-level privileges** on the host. Standardizing this workaround as an operational practice may incentivize:

- Granting broader administrative access to operational staff than otherwise necessary (violating least-privilege principles)
- Use of elevation techniques (e.g., scheduled tasks running as SYSTEM) that themselves introduce additional attack surface
- Increased blast radius if the account or script used to invoke `tscon` is compromised

---

## 4. Reduced Audit Visibility

Standard RDP connect/disconnect/logoff events generate specific, well-understood Windows Security Event Log entries (Event IDs such as 4778/4779, 4624/4634, etc.) that are commonly ingested by SIEM and monitoring tools. Session reattachment via `tscon` does not always generate equivalent, clearly distinguishable audit trail entries depending on OS version and configuration.

**Risk:** Security operations teams relying on standard RDP session telemetry may have **reduced visibility** into who accessed a given session and when, complicating incident response, forensic investigation, and compliance reporting (particularly relevant for regulated trading environments subject to audit requirements).

---

## 5. Detection as Malicious Activity by Security Tooling

Because `tscon`-based session hijacking is a recognized adversary technique, many commercial Endpoint Detection and Response (EDR) and antivirus solutions **flag or block `tscon` invocations** — particularly when combined with elevation tools — as suspicious or malicious behavior.

**Risk:**
- Legitimate use of this workaround may trigger security alerts, requiring exception handling or allow-listing that weakens detection fidelity for genuine attacks using the same technique.
- Conversely, if the workaround is allow-listed broadly, it may create a blind spot that an actual attacker could exploit using the identical command.

---

## 6. Licensing and Session Accounting Ambiguity

Windows Remote Desktop Services licensing and concurrent session limits are generally designed around the assumption of standard connect/disconnect/logoff behavior. Using `tscon` to persist a console-bound session independent of an active RDP connection may create ambiguity in:

- Concurrent Remote Desktop Services Client Access License (RDS CAL) accounting
- Session limit enforcement on servers configured for multiple concurrent users

This is a licensing/compliance consideration separate from, but related to, security risk, and should be reviewed with internal licensing or vendor compliance teams.

---

## 7. No Idle Timeout or Automatic Re-Lock Enforcement

Because the session is deliberately kept active and bound to the console to preserve IB Gateway's authentication state, standard idle-timeout and automatic screen-lock policies that would normally apply to a disconnected or logged-off RDP session **may not trigger** as expected. This can result in indefinitely unlocked, unattended sessions running live trading infrastructure.

---

## Recommended Compensating Controls

Clients who determine that the operational benefit of this workaround outweighs its risks should consider implementing the following compensating controls:

1. **Restrict administrative access** to the server to the minimum necessary set of individuals or service accounts, and avoid shared administrative credentials.
2. **Enforce physical and console-level security** for any machine where this workaround is deployed, including restricting physical/hypervisor console access and disabling unnecessary remote console tools (IPMI, iDRAC, iLO, hypervisor consoles) where not required.
3. **Implement independent session monitoring** (e.g., via Sysmon, enhanced Windows auditing, or third-party EDR) specifically configured to log and alert on `tscon` usage and session reattachment events, rather than relying on default RDP event logging alone.
4. **Avoid using SYSTEM-level elevation techniques** (e.g., scheduled tasks running as SYSTEM) to invoke `tscon`; where possible, scope execution to the same user account that owns the session.
5. **Apply network-level segmentation and firewalling** to limit which hosts/users can establish RDP connections to the server in question.
6. **Document and periodically review** the use of this workaround as part of the organization's change management and security review processes, given its deviation from standard, vendor-supported session handling.
7. **Consider alternative architectures** — such as dedicated always-on virtual displays, supported remote access solutions designed for unattended GUI persistence, or vendor-supported headless automation (where available) — that avoid the underlying session-detachment problem without relying on a console-reattachment technique.

---

## Disclaimer

As stated in the originating whitepaper, Interactive Brokers does not design, test, or support custom remote access configurations, including use of the `tscon` command. The security considerations outlined in this addendum are provided for client awareness and risk evaluation purposes only and do not constitute an exhaustive security assessment. Clients should engage their internal information security and compliance teams prior to adopting this or any similar workaround in a production trading environment.
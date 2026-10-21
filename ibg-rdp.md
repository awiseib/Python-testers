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
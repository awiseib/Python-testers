# Interactive Brokers TWS API — Python Sample Requests

> **Proof of Concept — Not Production Code**
>
> These scripts are intended solely to clarify implementation details and demonstrate how specific TWS API requests can be constructed using Python. They are **not** hardened for production use.
>
> **Always test in a Paper Trading account.** Do not run against a live brokerage account unless you have been explicitly instructed to do so by Interactive Brokers Client Services.

---

## Purpose

This repository contains sample Python scripts that exercise the [Interactive Brokers TWS API](https://ibkrcampus.com/ibkr-api-page/twsapi-doc/). Each script targets a narrow use case — placing a single order type, querying account data, subscribing to market data, etc. — and is written to be read alongside the official documentation, not deployed as-is.

Use these samples to:

- Understand the request/response lifecycle for a given API call
- Confirm field names, data types, and parameter constraints
- Reproduce or investigate a specific behavior before filing a support ticket

## Prerequisites

- Python 3.12
- TWS or IB Gateway running locally with the API enabled
- The `ibapi` client library (included in the TWS API download)
  - `pip install ibapi` does not install the correct release. See the [Official TWS API Documentation](https://www.interactivebrokers.com/docs/tws-api/doc/download-the-tws-api/introduction) for details.
- A **Paper Trading** account configured in TWS/Gateway

## Disclaimer

These scripts are provided as-is for educational and debugging purposes. Interactive Brokers and the repository maintainer make no warranty regarding their fitness for any particular purpose. Execution of orders in a live account using unreviewed code carries financial risk. Review all code carefully before use.

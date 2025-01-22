## GitHub Copilot Chat

- Extension Version: 0.23.2 (prod)
- VS Code: vscode/1.96.4
- OS: Windows

## Network

User Settings:
```json
  "github.copilot.advanced.debug.useElectronFetcher": true,
  "github.copilot.advanced.debug.useNodeFetcher": false,
  "github.copilot.advanced.debug.useNodeFetchFetcher": true
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 20.207.73.85 (59 ms)
- DNS ipv6 Lookup: Error (104 ms): getaddrinfo ENOTFOUND api.github.com
- Proxy URL: None (8 ms)
- Electron fetch (configured): HTTP 200 (898 ms)
- Node.js https: HTTP 200 (507 ms)
- Node.js fetch: HTTP 200 (613 ms)
- Helix fetch: HTTP 200 (400 ms)

Connecting to https://api.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.114.22 (297 ms)
- DNS ipv6 Lookup: Error (6 ms): getaddrinfo ENOTFOUND api.githubcopilot.com
- Proxy URL: None (1 ms)
- Electron fetch (configured): HTTP 200 (2123 ms)
- Node.js https: HTTP 200 (1429 ms)
- Node.js fetch: HTTP 200 (1418 ms)
- Helix fetch: HTTP 200 (1223 ms)

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).
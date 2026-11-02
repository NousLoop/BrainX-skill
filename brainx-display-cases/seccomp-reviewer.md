# Nested reviewer sandbox profile

Source: https://github.com/moby/profiles/blob/4b8214fc4971e06172938a1f1554ccff6647ee80/seccomp/default.json
License: Apache-2.0 (https://github.com/moby/profiles/blob/4b8214fc4971e06172938a1f1554ccff6647ee80/LICENSE)

Retain the upstream Docker default profile and add one allow rule for
`unshare, mount, mount_setattr, pivot_root, umount2, clone`. Codex 0.166.0 uses unprivileged bubblewrap
namespaces for read-only execution; Docker's default filter blocks those calls.
Kernel namespace/capability checks remain active. Do not add SYS_ADMIN,
privileged mode or an unconfined seccomp profile. The allowed namespace syscall
surface increases, but host administrative capabilities are not granted.

Before paid runs verify that the sandbox can read a probe and rejects writes
to a directory writable outside the sandbox. `smoke-test-reviewer.py` checks
this and the MCP/App Server handshake. Record the profile hash and preserve
earlier attempts when changing the environment baseline.

#!/bin/sh

echo STABLE_GIT_COMMIT "$(git describe --no-match --always --dirty)"

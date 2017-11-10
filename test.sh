#!/bin/sh
trendt --help
echo ""
trendt \
  --from 2013-01-01 \
  --to 2017-01-01 \
  --github-oauth-token 0b5af754b0261a50bc22ae53f718f13d8573a03f \
  docker

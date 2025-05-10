# RhythmFusion/Justfile

FRONTEND := "frontend"

default:
    @cd {{FRONTEND}} && just

run:
    @cd {{FRONTEND}} && just run

type-check:
    @cd {{FRONTEND}} && just type-check

build-only:
    @cd {{FRONTEND}} && just build-only

build:
    @cd {{FRONTEND}} && just build

preview:
    @cd {{FRONTEND}} && just preview

lint:
    @cd {{FRONTEND}} && just lint

format:
    @cd {{FRONTEND}} && just format

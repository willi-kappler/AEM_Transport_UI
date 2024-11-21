{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    nativeBuildInputs = with pkgs.buildPackages; [
      (python312.withPackages(ps: with ps; [
        fastapi
        flake8
        ipython
        jinja2
        python-multipart
        mypy
        uvicorn
        pydantic
        ]))
      pyright
      ruff
    ];
}


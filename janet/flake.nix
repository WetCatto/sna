{
  description = "janet: an implementation of a social diffusion model";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs   = import nixpkgs { inherit system; };
          python = pkgs.python314;

          types-networkx = pkgs.python314Packages.buildPythonPackage rec {
            pname = "types-networkx";
            version = "3.6.1.20260408";
            format = "other";

            src = pkgs.python314Packages.fetchPypi {
              inherit version;
              pname = "types_networkx";
              hash = "sha256-Y/lJArLZnW1PRI6xvCO4oyfUAi9QmLwNItQrEwA7EG4=";
            };
            
            # Manually copy the stubs into the Python site-packages directory
            installPhase = ''
              runHook preInstall
    
              # Create the site-packages directory for Python 3.14
              TARGET_DIR=$out/lib/python${python.pythonVersion}/site-packages
              mkdir -p $TARGET_DIR
    
              # Copy the 'networkx-stubs' directory to the target
              # These packages usually contain a directory named 'networkx-stubs'
              if [ -d "networkx-stubs" ]; then
                cp -r networkx-stubs $TARGET_DIR/
              else
              # Fallback: copy everything if the structure is flat
                cp -r * $TARGET_DIR/
              fi
    
              runHook postInstall
            '';

            doCheck = false;
          };
      
          # Python environment
          py-env = python.withPackages (ps: with ps; [
            # Core libraries
            numpy          # Multi-dimensional arrays
            scipy          # Advanced scientific computations
            matplotlib     # Network plotting
            networkx       # Network library
            types-networkx # Typing stubs for networkx
            
            # Development libraries
            ipython    # Interactive computations
            pytest     # Testing
            pytest-cov # Test coverage
            ruff       # Linter
            mypy       # Typechecker
          ]);

          typst-utils = with pkgs; [
            typst      # Compiler
            tinymist   # LSP
            typstyle   # Formatter
            typst-live # Previewer
          ];

          other-utils = with pkgs; [
            just         # Command runner
            helix        # Text editor
            basedpyright # Python LSP
          ];
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            py-env
            typst-utils
            other-utils
          ];

          shellHook = ''
            export PYTHONPATH="$PWD:$PYTHONPATH"
          '';
        };

        packages.default = python.pkgs.buildPythonPackage {
          pname = "janet";
          version = "0.1.1";
          src = pkgs.lib.cleanSource self;
          pyproject = true;

          build-system = with python.pkgs; [
            setuptools
          ];

          dependencies = with python.pkgs; [
            numpy
            scipy
            matplotlib
          ];
        };  
      });
}

{
  buildPythonPackage,
  fetchPypi,
  robotpy-wpiutil,
  lib,
}:
buildPythonPackage rec {
  pname = "robotpy-wpinet";
  version = "2024.3.2.1";
  format = "wheel";

  src = fetchPypi {
    inherit version format;
    pname = builtins.replaceStrings ["-"] ["_"] pname;
    hash = "sha256-ePo02yg0O9jggcvjyYGwCyoMdoLPwFK60hUnd+BqswU=";

    abi = "cp312";
    dist = "cp312";
    python = "cp312";
    platform = "manylinux_2_35_x86_64";
  };

  dependencies = [
    robotpy-wpiutil
  ];

  meta = {
    homepage = "https://robotpy.github.io/";
    license = lib.licenses.bsd3;
    # maintainers = with lib.maintainers; [archb1w];
    platforms = ["x86_64-linux"];
  };
}

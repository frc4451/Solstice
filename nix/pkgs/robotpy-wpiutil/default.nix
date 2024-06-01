{
  buildPythonPackage,
  fetchPypi,
  lib,
}:
buildPythonPackage rec {
  pname = "robotpy-wpiutil";
  version = "2024.3.2.1";
  format = "wheel";

  src = fetchPypi {
    inherit version format;
    pname = builtins.replaceStrings ["-"] ["_"] pname;
    hash = "sha256-0HXDenxJOGE3tsldDqM6R/QrzfBYtzgLah9KCFO2rzk=";

    abi = "cp312";
    dist = "cp312";
    python = "cp312";
    platform = "manylinux_2_35_x86_64";
  };

  meta = {
    homepage = "https://robotpy.github.io/";
    license = lib.licenses.bsd3;
    # maintainers = with lib.maintainers; [archb1w];
    platforms = ["x86_64-linux"];
  };
}

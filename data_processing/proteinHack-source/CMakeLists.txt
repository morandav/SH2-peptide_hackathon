cmake_minimum_required(VERSION 3.20)
project(proteinHack)

set(CMAKE_CXX_STANDARD 14)

add_executable(proteinHack Vector3.cc Atom.cc Rotation3.cc Matrix3.cc RigidTrans3.cc Triangle.cc PDB.cc Match.cc numerics.cc structAlign.cc)

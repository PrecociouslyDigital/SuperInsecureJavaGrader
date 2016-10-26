import subprocess
from os import remove
def evaluateWork(fileName, name):
    print("Evaluating: " + fileName)
    program = ""
    with open(fileName, "r") as progra:
        program = progra.read()
    with open("results.dat", "a") as results:
        result = subprocess.run(["javac", fileName], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode != 0:
            print(result.stdout)
            print("Something broke")
            results.write("\n\n".join(
                ["",
                "-----",
                name+": Did not compile!",
                result.stdout,
                "File was",
                program]))
        else:
            results.write("\n\n".join(
                            ["",
                            "-----",
                            name + ": Compiled",
                            "File was",
                            program]))
            fileName = fileName.split(".")[0]
            with open("tests.dat", "r") as tests:
                testsList = tests.read().split("-----")
                for test in testsList:
                    parts = test.split("---")
                    results.write("\n\n---\n\nTesting " + parts[0] +"\nShould be: " + parts[1] +"\n\n")
                    result = subprocess.run(["java", fileName], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, input=parts[0])
                    if result.returncode!=0:
                        results.write("\n\n".join(
                        ["Some Error!",
                        "Output was:\n" + result.stdout]))
                    else:
                        theResults = result.stdout.strip()
                        if theResults == parts[1]:
                            results.write("\n\nCorrect!\n\n")
                        else:
                            results.write("\n\n".join(
                            ["Not Correct!",
                            "Output was:\n" + theResults]))
            remove(fileName + ".class")
        remove(fileName + ".java")

if __name__ == "__main__":
    evaluateWork("Test.java", "Ben")

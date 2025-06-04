from setuptools import setup,find_packages
from typing import List 

HYPEN_E_DOT = "-e ."

def getrequirements()-> List[str]:
    """
    Returns:
        List[str]: _description_ 
    """
    requirements=[]

    try:
        with open("requirements.txt", 'r') as f:
            requirements = f.readlines()
            requirements = [req.strip("\n") for req in requirements]
            if HYPEN_E_DOT in requirements:
                requirements.remove(HYPEN_E_DOT)
            return requirements
    except Exception as E:
        print(E)


setup(
    name="NetworkSecurity",
    description="this is my second project following krish naik's ml course ",
    author_email="kgopinath730@gmail.com",
    packages=find_packages(),
    install_requires=getrequirements()

)

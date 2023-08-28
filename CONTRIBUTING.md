# Contributing to python-mysql-replication

Firstly, thank you for considering to contribute to `python-mysql-replication`. We appreciate your effort, and to ensure that your contributions align with the project's coding standards, we employ the use of `pre-commit` hooks. This guide will walk you through setting them up.

## Setting up pre-commit

1. **Install pre-commit**

   Before you can use `pre-commit`, you need to install it. You can do so using `pip`:

   ```bash
   pip install pre-commit
   ```

2. **Install the pre-commit hooks**

   Navigate to the root directory of your cloned `python-mysql-replication` repository and run:

   ```bash
   pre-commit install
   ```

   This will install the `pre-commit` hooks to your local repository.

3. **Make sure to stage your changes**

   `pre-commit` will only check the files that are staged in git. So make sure to `git add` any new changes you made before running `pre-commit`.

4. **Run pre-commit manually (Optional)**

   Before committing, you can manually run:

   ```bash
   pre-commit run --all-files
   ```

   This will run the hooks on all the files. If there's any issue, the hooks will let you know.

## If you encounter issues

If you run into any problems with the hooks, you can always skip them using:

```bash
git commit -m "Your commit message" --no-verify
```

However, please note that skipping hooks might lead to CI failures if we use these checks in our CI pipeline. It's always recommended to adhere to the checks to ensure a smooth contribution process.

---

That's it! With these steps, you should be well on your way to contributing to `python-mysql-replication`. We look forward to your contributions! 

---

package main

import (
	"fmt"
	"log"
	"os"

	"github.com/go-git/go-git/v5"
	"github.com/go-git/go-git/v5/plumbing"
)

func main() {
	sourceRepoBranch := "feature/something"
	sourceRepoPath := "/tmp/foo/source"
	sourceRepoUrl := "https://github.com/go-git/go-git"

	// targetRepoBranch := "feature/something-else"
	targetRepoPath := "/tmp/foo/target"
	targetRepoUrl := "https://github.com/go-git/go-git"

	_, err := os.Stat(sourceRepoPath)
	if os.IsNotExist(err) {
		_, err := git.PlainClone(
			sourceRepoPath,
			false,
			&git.CloneOptions{
				URL:      sourceRepoUrl,
				Progress: os.Stdout,
			})
		if err != nil {
			_ = fmt.Errorf("failed cloning the source repository: %w", err)
		}
	}
	sourceRepo, err := git.PlainOpen(sourceRepoPath)
	if err != nil {
		_ = fmt.Errorf("failed opening the source repository: %w", err)
	}
	log.Printf("sourceRepo: %+v", sourceRepo)

	_, err = os.Stat(targetRepoPath)
	if os.IsNotExist(err) {
		_, err := git.PlainClone(
			targetRepoPath,
			false,
			&git.CloneOptions{
				URL:      targetRepoUrl,
				Progress: os.Stdout,
			})
		if err != nil {
			_ = fmt.Errorf("failed cloning the target repository: %w", err)
		}
	}
	targetRepo, err := git.PlainOpen(targetRepoPath)
	if err != nil {
		_ = fmt.Errorf("failed cloning the target repository: %w", err)
	}
	log.Printf("targetRepo: %+v", targetRepo)

	// FIXME
	// Does not seem to change branch.

	currentBranch, err := sourceRepo.Head()
	if err != nil {
		_ = fmt.Errorf("failed getting the current branch of the source repository: %w", err)
	}
	log.Printf("current branch of the source repository: %s", currentBranch.Name().Short())

	if currentBranch.Name().Short() != sourceRepoBranch {
		wt, err := sourceRepo.Worktree()
		if err != nil {
			_ = fmt.Errorf("failed getting the source repository's worktree: %w", err)
		}

		err = wt.Checkout(&git.CheckoutOptions{Branch: plumbing.ReferenceName(sourceRepoBranch)})
		if err != nil {
			_ = fmt.Errorf("failed switching branch in the source repository: %w", err)
		}

		currentBranch, err = sourceRepo.Head()
		if err != nil {
			_ = fmt.Errorf("failed getting the current branch of the source repository: %w", err)
		}
		log.Printf("changed branch of the source repository to %s", currentBranch.Name().Short())
	}
}

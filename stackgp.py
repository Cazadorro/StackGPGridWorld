#!/bin/bash
import random

UNIT_DISTRIBUTION_DEVIATION = 1 / 3


def random_unit_normalized_distribution():
    return random.gauss(0, UNIT_DISTRIBUTION_DEVIATION)


def clamp(mine_val, min_val=0, max_val=1):
    return max(min(mine_val, max_val), min_val)


def clamp_list(mine_val_list, min_val=0, max_val=1):
    clamped_list = mine_val_list[:]
    for i in range(len(clamped_list)):
        clamped_list[i] = clamp(clamped_list, min_val, max_val)
    return clamped_list


def roll_accepted(normalized_probability):
    return True if (random.random() < normalized_probability) else False


def get_mutated(normalized_gene):
    return clamp(normalized_gene + random_unit_normalized_distribution())


def attempt_mutation(normalized_gene, normalized_probability):
    if roll_accepted(normalized_probability):
        return get_mutated(normalized_gene)
    return normalized_gene


class Bounds:
    def __init__(self, lower_bound, upper_bound=None):
        if upper_bound is not None:
            self.lower = lower_bound
            self.upper = upper_bound
        else:
            self.lower = 0
            self.upper = lower_bound

    def set_upper_bound(self, upper_bound):
        self.upper = upper_bound

    def set_lower_bound(self, lower_bound):
        self.lower = lower_bound

    def set_bounds(self, lower_bound, upper_bound=None):
        if upper_bound is not None:
            self.lower = lower_bound
            self.upper = upper_bound
        else:
            self.lower = 0
            self.upper = lower_bound

    def check_inclusive_lower(self, value_tested):
        return True if value_tested >= self.lower else False

    def check_inclusive_upper(self, value_tested):
        return True if value_tested <= self.upper else False

    def check_inclusive(self, value_tested):
        lower_inclusive = self.check_inclusive_lower(value_tested)
        upper_inclusive = self.check_inclusive_upper(value_tested)
        return True if (lower_inclusive and upper_inclusive) else False

    def check_inclusive_exclusive(self, value_tested):
        lower_inclusive = self.check_inclusive_lower(value_tested)
        upper_exclusive = self.check_exclusive_upper(value_tested)
        return True if (lower_inclusive and upper_exclusive) else False

    def check_exclusive_inclusive(self, value_tested):
        lower_exclusive = self.check_exclusive_lower(value_tested)
        upper_inclusive = self.check_inclusive_upper(value_tested)
        return True if (lower_exclusive and upper_inclusive) else False

    def check_exclusive_lower(self, value_tested):
        return True if value_tested > self.lower else False

    def check_exclusive_upper(self, value_tested):
        return True if value_tested < self.upper else False

    def in_exclusive(self, value_tested):
        lower_exclusive = self.check_exclusive_lower(value_tested)
        upper_exclusive = self.check_exclusive_upper(value_tested)
        return True if (lower_exclusive and upper_exclusive) else False


class AcceptanceCheckDice:
    def __init__(self, lower_range, upper_range):
        self.lower_range = lower_range
        self.upper_range = upper_range

    def roll_is_accepted(self, bounds):
        roll_value = random.uniform(self.lower_range, self.upper_range)
        return bounds.check_inclusive(roll_value)

    def set_range(self, lower_range, upper_range):
        self.lower_range = lower_range
        self.upper_range = upper_range


class StackGenotype:
    def __init__(self, gp_op_handle, mutation_coefficients, mutation_chance):
        self.op_handle = gp_op_handle
        self.mutation_coefficients = mutation_coefficients
        self.mutation_chance = mutation_chance

    def evaluate(self, gp_operators):
        """
        evaluates the member, assumes variables have been set outside for terminals
        :return:
        """
        return self.op_handle.evaluate(gp_operators)

    @classmethod
    def from_mutation(cls, stack_genotype):
        new_mutation_chance = stack_genotype.mutation_chance

        if mutation_dice.roll_is_accepted(mutation_bounds):
            new_mutation_chance += random.gauss(0, 1)  # bound this
        new_mutation_coefficients = normalized_genotype.from_uniform_mutation(stack_genotype.mutation_coefficients,
                                                                              mutation_chance)
        for i in range(len(new_mutation_coefficients)):
            if mutation_dice.roll_is_accepted(mutation_bounds):
                new_mutation_coefficients[i] += random.gauss(0, 1)
        new_op_handle = stack_genotype.gp_op_handle
        for i in range(len(new_op_handle)):
            if mutation_dice.roll_is_accepted(mutation_bounds):
                new_op_handle[i] = random.randint


class normalized_genotype:
    def __init__(self, normalized_genes):
        self.genes = clamp_list(normalized_genes)

    @classmethod
    def from_uniform_mutation(cls, normalized_genotype, mutation_probability):
        mutated_genes = normalized_genotype.genes
        for i in range(len(mutated_genes)):
            mutated_genes[i] = attempt_mutation(mutated_genes, mutation_probability)
        return normalized_genotype(mutated_genes)

    @classmethod
    def from_uniform_random(cls, length):
        random_genes = [random.random() for _ in range(length)]
        return normalized_genotype(random_genes)


class GPOperatorHandle:
    def __init__(self, gp_index_list):
        self.index_list = gp_index_list

    def evaluate(self, gp_operators):
        stack = []
        for index in self.index_list:
            assert (index < len(gp_operators)), "Error, index exceeds length of operators"
            gp_operators[index](stack)
        return stack

    @classmethod
    def uniform_initialization(cls, min_op_index, max_op_index, size):
        gp_index_list = [random.randint(min_op_index, max_op_index) for _ in range(size)]
        return GPOperatorHandle(gp_index_list)

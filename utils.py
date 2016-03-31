def typecheck(args, expectedArgTypes):
	"""
		A quick pass at a type-checking function to validate input arguments for other functions.
		
		Params:

		- args: list containing all input args to the calling function, of the form:

			[arg1, arg2, ...., argn]

		- expectedArgTypes: list of each input arg's expected type, of the form:
			
			[expectedType1, expectedType2, ..., expectedTypeN]

		Raises:
			TypeError if any arguments do not match their expected type.

		Returns: 
		- None, if all arguments have valid types.
	"""
	if not isinstance(args, list) or not isinstance(expectedArgTypes, list):
		raise TypeError("typecheck takes two arrays where array 1 is the args, and array 2 is the types")
	if len(args) != len(expectedArgTypes):
		raise ValueError("typecheck input arrays must be of the same length")
	for i in range(len(args)):
		if not isinstance(args[i], expectedArgTypes[i]):
			raise TypeError("Input arg #{0}: '{1}'' must be of type {2}, was type {3}".format(i, args[i], expectedArgTypes[i], type(args[i])))
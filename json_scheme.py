data_scheme = \
    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "board": {
                "type": "object",
                "properties": {
                    "walkers": {
                        "type": "array",
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string"
                                    },
                                    "values": {
                                        "type": "object",
                                        "properties": {
                                            "num": {
                                                "type": "integer"
                                            }
                                        },
                                        "required": [
                                            "num"
                                        ]
                                    }
                                },
                                "required": [
                                    "type",
                                    "values"
                                ]
                            },
                            {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string"
                                    },
                                    "values": {
                                        "type": "object",
                                        "properties": {
                                            "num": {
                                                "type": "integer"
                                            },
                                            "direction": {
                                                "type": "string"
                                            },
                                            "weight": {
                                                "type": "number"
                                            }
                                        },
                                        "required": [
                                            "num",
                                            "direction",
                                            "weight"
                                        ]
                                    }
                                },
                                "required": [
                                    "type",
                                    "values"
                                ]
                            },
                            {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string"
                                    },
                                    "values": {
                                        "type": "object",
                                        "properties": {
                                            "num": {
                                                "type": "integer"
                                            },
                                            "charge": {
                                                "type": "number"
                                            }
                                        },
                                        "required": [
                                            "num",
                                            "charge"
                                        ]
                                    }
                                },
                                "required": [
                                    "type",
                                    "values"
                                ]
                            }
                        ]
                    },
                    "obstacles": {
                        "type": "array",
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string"
                                    },
                                    "radius": {
                                        "type": "number"
                                    },
                                    "center": {
                                        "type": "array",
                                        "items": [
                                            {
                                                "type": "number"
                                            },
                                            {
                                                "type": "number"
                                            }
                                        ]
                                    },
                                    "charge": {
                                        "type": "number"
                                    }
                                },
                                "required": [
                                    "type",
                                    "radius",
                                    "center",
                                    "charge"
                                ]
                            },
                            {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string"
                                    },
                                    "width": {
                                        "type": "number"
                                    },
                                    "height": {
                                        "type": "number"
                                    },
                                    "start_point": {
                                        "type": "array",
                                        "items": [
                                            {
                                                "type": "number"
                                            },
                                            {
                                                "type": "number"
                                            }
                                        ]
                                    },
                                    "charge": {
                                        "type": "number"
                                    }
                                },
                                "required": [
                                    "type",
                                    "width",
                                    "height",
                                    "start_point",
                                    "charge"
                                ]
                            }
                        ]
                    },
                    "magical_gates": {
                        "type": "array",
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string"
                                    },
                                    "radius": {
                                        "type": "number"
                                    },
                                    "center": {
                                        "type": "array",
                                        "items": [
                                            {
                                                "type": "number"
                                            },
                                            {
                                                "type": "number"
                                            }
                                        ]
                                    },
                                    "end_point": {
                                        "type": "array",
                                        "items": [
                                            {
                                                "type": "number"
                                            },
                                            {
                                                "type": "number"
                                            }
                                        ]
                                    }
                                },
                                "required": [
                                    "type",
                                    "radius",
                                    "center",
                                    "end_point"
                                ]
                            },
                            {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string"
                                    },
                                    "width": {
                                        "type": "number"
                                    },
                                    "height": {
                                        "type": "number"
                                    },
                                    "start_point": {
                                        "type": "array",
                                        "items": [
                                            {
                                                "type": "number"
                                            },
                                            {
                                                "type": "number"
                                            }
                                        ]
                                    },
                                    "end_point": {
                                        "type": "array",
                                        "items": [
                                            {
                                                "type": "number"
                                            },
                                            {
                                                "type": "number"
                                            }
                                        ]
                                    }
                                },
                                "required": [
                                    "type",
                                    "width",
                                    "height",
                                    "start_point",
                                    "end_point"
                                ]
                            }
                        ]
                    }
                },
                "required": [
                    "walkers",
                    "obstacles",
                    "magical_gates"
                ]
            },
            "simulation": {
                "type": "object",
                "properties": {
                    "stop_param": {
                        "type": "integer"
                    },
                    "num_of_simulations": {
                        "type": "integer"
                    }
                },
                "required": [
                    "stop_param",
                    "num_of_simulations"
                ]
            },
            "stats": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string"
                    },
                    "path": {
                        "type": "string"
                    }
                },
                "required": [
                    "type",
                    "path"
                ]
            }
        },
        "required": [
            "board",
            "simulation",
            "stats"
        ]
    }
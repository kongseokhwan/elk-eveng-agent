function myAction(args) {
    const leftPad = require("left-pad")
    const lines = args.lines || [];
    return { "message" : "helloworld" }
}
exports.main = myAction;


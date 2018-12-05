print('bugprint') // does not print after refresh
// -----------------------

// Creating the blocks

var genBlock = function (w, h, xp, yp) {
  return {shape: 'rect', static: false, dims: [w, h], x:xp, y: yp}
}

var addBlock = function(yp, xDim) {
  var w = gaussian(20,8)
  var h = 20
  var xp = gaussian(Math.floor(xDim/2), 10)
  
  return genBlock(w,h,xp,yp)
}

var addBlocks = function(n) {
  var world = [].concat(addBlock(520-(n*40), 350))

  if(n > 1)
      return addBlocks(n - 1).concat(world)
  
  return world
}

var makeFloor = function (xmin, xmax, width) {
  return {shape: 'rect', static: true, dims: [400, 10], x: 175, y: 510}
          
}

// -----------------------

// Conditions

var enforceWorldStable = function(model) {
  return function() {
    var m = model()
    var finalState = physics.run(1000, m)
    condition(physics.compareShapes(m, finalState))
    return m
  }
}

var model = function() {
  var world = [].concat(makeFloor(-1000, 1000, 25))
  return world.concat(addBlocks(8))
}

// -----------------------

// Sampling

var enforcedModel = enforceWorldStable(model)

var out = Infer({method: 'rejection', samples:1}, enforcedModel)
physics.animate(1000, sample(out))